#include <Wire.h>

// I2C Arduino Slave

int MIC_SENSOR_PIN = 0;
uint16_t amplitude = 0;

const int sampleWindow = 50; // Sample window width in mS (50 mS = 20Hz)
unsigned int sample;

void setup() {
    Wire.begin(18);
    Wire.onRequest(requestEvent);
    Serial.begin(9600);
}

void loop() {
    readAmplitude();
    delay(1000);
}

void readAmplitude() {
    unsigned long startMillis= millis();

    unsigned int signalMax = 0;
    unsigned int signalMin = 1024;

    // collect data for 50 mS
    while (millis() - startMillis < sampleWindow) {
        sample = analogRead(MIC_SENSOR_PIN);
        if (sample < 1024) {
            if (sample > signalMax) {
                signalMax = sample;  // save just the max levels
            } else if (sample < signalMin) {
                signalMin = sample;  // save just the min levels
            }
        }
    }
   amplitude = signalMax - signalMin;

   //Serial.println(amplitude);
}

void requestEvent() {
    byte response_buffer[2];
    response_buffer[0] = (amplitude >> 8) & 0xFF;
    response_buffer[1] = amplitude & 0xFF;
    Wire.write(response_buffer, 2);

    Serial.print("Amplitude sent: ");
    Serial.print(response_buffer[0], DEC);
    Serial.print(",");
    Serial.println(response_buffer[1], DEC);
}

#include <Wire.h>
#include <RH_ASK.h>
#include <SPI.h>

RH_ASK driver;

// I2C Pro Trinket Slave

int MIC_SENSOR_PIN = 3;
int GAS_SENSOR_PIN = 2;
int RF_TRANSMITTER_PIN = 12;

uint16_t audio = 0;
uint16_t gas = 0;

char sensor;

const int sampleWindow = 50;
unsigned int sample;

void setup() {
    Wire.begin(12);
    Wire.onReceive(receiveData);
    Wire.onRequest(readData);

    Serial.begin(9600);
}

void loop() {
    audio = readMic();
    Serial.print("Audio: ");
    Serial.println(audio);
    gas = readGas();
    Serial.print("Gas: ");
    Serial.println(gas);
}

uint16_t readMic() {
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
   return signalMax - signalMin;
}

uint16_t readGas() {
    return analogRead(GAS_SENSOR_PIN);
}

void receiveData(int howMany) {
    Serial.print("howMany: ");
    Serial.println(howMany);
    while (0 < Wire.available()) {
        sensor = Wire.read();

        Serial.print("Receive Data: ");
        Serial.println(sensor);
    }
}

void readData() {
    byte response_buffer[2];
    uint16_t result = 0;

    if (sensor == 'A') {
        result = audio;
    } else if (sensor == 'G') {
        result = gas;
    } else if (sensor == 'T') {
        transmitData();
    }

    Serial.print("Read Data: ");
    Serial.println(result);
    
    response_buffer[0] = (result >> 8) & 0xFF;
    response_buffer[1] = result & 0xFF;
    Wire.write(response_buffer, 2);
}

void transmitData() {
    const char *msg = "Hello World!!";
    driver.send((uint8_t *)msg, strlen(msg) + 1);
    driver.waitPacketSent();
}


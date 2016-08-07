#include <Wire.h>
#include <RH_ASK.h>
#include <SPI.h>

RH_ASK driver;

// I2C Pro Trinket Slave

int MIC_SENSOR_PIN = 3;
int GAS_SENSOR_PIN = 2;
int RF_TRANSMITTER_PIN = 12;

byte response_buffer[2];
uint16_t audio = 0;
uint16_t gas = 0;
int read_index = 0;

char sensor;

const int sampleWindow = 50;
unsigned int sample;

void setup() {
    Wire.begin(18);
    Wire.onReceive(receiveData);
    Wire.onRequest(readData);
}

void loop() {
    audio = readMic();
    gas = readGas();
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
    while (0 < Wire.available()) {
        sensor = Wire.read();
    }
    read_index = 0;

    uint16_t result = 0;
    if (sensor == 'A') {
        result = audio;
    } else if (sensor == 'G') {
        result = 0xFF;
    }
    response_buffer[0] = (result >> 8) & 0xFF;
    response_buffer[1] = result & 0xFF;
}

void readData() {
    Wire.write(response_buffer[read_index]);
    read_index++;
}

void transmitData() {
    const char *msg = "Hello World!!";
    driver.send((uint8_t *)msg, strlen(msg) + 1);
    driver.waitPacketSent();
}


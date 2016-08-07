#include <Wire.h>

const int PIN_IO = 12;
const int PIN_MIC_SENSOR = 3;
const int PIN_GAS_SENSOR = 2;
const int PIN_LED = 13;

const int I2C_SLAVE_ADDR = 0x12;

byte response_buffer[2];
int read_index = 0;

uint16_t audio = 0;
uint16_t gas = 0;

const int sampleWindow = 50;
unsigned int sample;

int led_state = HIGH;

void setup() {
    pinMode(PIN_IO, OUTPUT);

    Wire.begin(I2C_SLAVE_ADDR);
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

    while (millis() - startMillis < sampleWindow) {
        sample = analogRead(PIN_MIC_SENSOR);
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
    return analogRead(PIN_GAS_SENSOR);
}

void receiveData(int howMany) {
    char command = 'U';
    while (0 < Wire.available()) {
        command = Wire.read();
        digitalWrite(PIN_LED, !led_state);
        led_state = !led_state;
    }

    uint16_t result = 0;
    if (command == 'A') {
        result = audio;
    } else if (command == 'G') {
        result = 0xFF;
    } else if (command == 'C') {
        digitalWrite(PIN_IO, LOW);
    } else if (command == 'S') {
        digitalWrite(PIN_IO, HIGH);
    }

    response_buffer[0] = (result >> 8) & 0xFF;
    response_buffer[1] = result & 0xFF;

    read_index = 0;
}

void readData() {
    Wire.write(response_buffer[read_index]);
    read_index++;
}


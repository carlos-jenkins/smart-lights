#include <RH_ASK.h>
#include <SPI.h> // Not actually used but needed to compile

const int PIN_IO = 4;
const int PIN_LED = 13;

RH_ASK driver;

void setup() {

    pinMode(PIN_IO, OUTPUT);
    pinMode(PIN_LED, OUTPUT);

    Serial.begin(115200);

    if (!driver.init()) {
        Serial.println("Initialization failed");
    }
}

char buf[64];

void loop() {
    uint8_t received = sizeof(buf);
    if (driver.recv((uint8_t *)buf, &received)) {
        buf[received] = '\0';

        if (buf[0] == 'S') {
            digitalWrite(PIN_IO, LOW);
            digitalWrite(PIN_LED, LOW);
        } else if (buf[0] == 'C') {
            digitalWrite(PIN_IO, HIGH);
            digitalWrite(PIN_LED, HIGH);
        }
    }
}

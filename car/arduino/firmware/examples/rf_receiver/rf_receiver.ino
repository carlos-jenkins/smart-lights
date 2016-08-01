#include <RH_ASK.h>
#include <SPI.h> // Not actually used but needed to compile

RH_ASK driver;

void setup() {
    Serial.begin(9600);
    if (!driver.init()) {
        Serial.println("init failed");
    }
}

char buf[64];

void loop() {
    uint8_t received = sizeof(buf);
    if (driver.recv((uint8_t *)buf, &received)) {
        buf[received] = '\0';
        Serial.print("Message: (");
        Serial.print(received);
        Serial.print(") ");
        Serial.println(buf);
    }
}

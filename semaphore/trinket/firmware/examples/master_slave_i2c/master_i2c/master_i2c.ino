#include <Wire.h>

// I2C Arduino Master

uint16_t amplitude = 0;
byte a,b;

void setup() {
    Wire.begin();
    Serial.begin(9600);
}

void loop() {
    Wire.requestFrom(18, 2);

    a = Wire.read();
    b = Wire.read();

    amplitude = a;
    amplitude = amplitude << 8 | b;

    Serial.print("Amplitude received: ");
    Serial.println(amplitude);

    delay(1000);
}

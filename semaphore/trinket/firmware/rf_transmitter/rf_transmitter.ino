#include <RH_ASK.h>
#include <SPI.h> // Not actually used but needed to compile

const int PIN_IO = 4;
const int PIN_LED = 13;

RH_ASK driver;
int led_state = LOW;

void setup()
{
    pinMode(PIN_IO, INPUT_PULLUP);
    pinMode(PIN_LED, OUTPUT);

    Serial.begin(115200);

    if (!driver.init())
         Serial.println("Initialization failed");
}

char msg[2] = {'S', '\0'};

void loop()
{
    int io_state = digitalRead(PIN_IO);
    if (io_state) {
        msg[0] = 'S';
    } else {
        msg[0] = 'C';
    }
    driver.send((uint8_t *)msg, sizeof(msg));
    driver.waitPacketSent();

    digitalWrite(PIN_LED, led_state);
    led_state = !led_state;
}


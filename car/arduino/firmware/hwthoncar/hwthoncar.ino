#include <Servo.h>

const int PIN_IO = A0;

const int PIN_LEFT_SERVO = 10;
const int PIN_RIGHT_SERVO = 9;
const int PIN_LED = 4;
const int PIN_LED_IO = 13;
const int PIN_SWITCH = 5;


Servo left_servo;
Servo right_servo;
const int STOP = 90;
const int FULL_LEFT = 0;
const int FULL_RIGHT = 180;


void setup() {
    left_servo.attach(PIN_LEFT_SERVO);
    right_servo.attach(PIN_RIGHT_SERVO);

    pinMode(PIN_IO, INPUT);
    pinMode(PIN_LED, OUTPUT);
    pinMode(PIN_SWITCH, INPUT_PULLUP);

    Serial.begin(115200);
}


void loop() {

    int switch_state = digitalRead(PIN_SWITCH);
    int io_state = digitalRead(PIN_IO);

    digitalWrite(PIN_LED, switch_state);
    digitalWrite(PIN_LED_IO, io_state);

    if (switch_state || !io_state) {
        left_servo.write(STOP);
        right_servo.write(STOP);

    } else {
         left_servo.write(FULL_LEFT);
         right_servo.write(FULL_RIGHT);
    }
}


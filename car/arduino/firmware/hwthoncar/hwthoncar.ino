#include <Servo.h>
#include <RH_ASK.h>
#include <SPI.h> // Not actually used but needed to compile RadioHead

const int pin_receiver = 11;
const int pin_left_servo = 10;
const int pin_right_servo = 9;
const int pin_led = 4;
const int pin_switch = 5;


Servo left_servo;
Servo right_servo;
const int STOP = 90;
const int FULL_SPEED = 180;


RH_ASK receiver;


void setup() {
    left_servo.attach(pin_left_servo);
    right_servo.attach(pin_right_servo);

    pinMode(pin_led, OUTPUT);
    pinMode(pin_switch, INPUT_PULLUP);

    Serial.begin(115200);
    if (!receiver.init()) {
        Serial.println("Receiver initialization failed!");
    }
}


char buf[64];

char get_semaphore_state() {

    uint8_t received = sizeof(buf);

    if (receiver.recv((uint8_t *)buf, &received)) {

        // Always terminate the string
        buf[received] = '\0';

        if (received != 1) {
            return 'E';
        }

        // Stop command
        if (buf[0] == 'S') {
            return 'S';
        }

        // Continue command
        if (buf[0] == 'C') {
            return 'C';
        }

        // Unknown command
        return 'U';
    }

    // Missing command
    return 'M';
}


void loop() {

    int switch_state = digitalRead(pin_switch);

    // If switch is HIGH stop everything
    if(switch_state == HIGH) {

        digitalWrite(pin_led, HIGH);
        left_servo.write(STOP);
        right_servo.write(STOP);

    } else {

        digitalWrite(pin_led, LOW);
        char semaphore_state = get_semaphore_state();

        if (semaphore_state == 'C') {
            left_servo.write(FULL_SPEED);
            right_servo.write(FULL_SPEED);

        } else if (semaphore_state == 'S') {
            left_servo.write(STOP);
            right_servo.write(STOP);

        } else {
            Serial.print("Command: ");
            Serial.println(semaphore_state);
        }
    }
}


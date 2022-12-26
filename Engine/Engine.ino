#include <Servo.h>

// Konfigurasi Servo
const uint8_t SERVO_PIN = D2;
Servo servo;

// Konfigurasi buzzer & push button
const uint8_t BUZZER_PIN = D0;
const uint8_t PUSH_BUTTON_PIN = D1;

void setup() {
  // Buka serial pembacaan data ke komputer
  Serial.begin(9600);
  Serial.setTimeout(1);

  // Konfigurasi Servo
  servo.attach(SERVO_PIN, 500, 2400);
  servo.write(0);

  // Konfigurasi buzzer dan tombol
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(PUSH_BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  // Kalau tombol dipencet, ya dibuka bae
  if (digitalRead(PUSH_BUTTON_PIN) == LOW) {
    unlockDoor();
    return;
  }

  // Kalau bukan dari serial, skip
  if (Serial.available() == 0) return;

  // Panggil serialnya di sini
  switch (Serial.readString().toInt()) {
    // Case: Handshake/Pinging Python ke Mikrokontroler
    case 0: animateBuzzer(4, 500); break;
    // Case: Buka pintu
    case 1: unlockDoor(); break; 
    // Case: Intruders alert
    case 2: animateBuzzer(10, 500); break;
  }
}
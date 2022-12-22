#include <Servo.h>

// Konfigurasi Servo
const uint8_t SERVO_PIN = D0;
Servo servo;

void animateServo(int count, long delayMs, bool is90Degree = true) {
  if (count < 1) return;
  for (int i = 0; i < count; i++) {
    if (i != 0) delay(delayMs);
    servo.write(is90Degree ? 90 : 180);
    delay(delayMs);
    servo.write(0);
  }
}

void setup() {
  // Buka serial pembacaan data ke komputer
  Serial.begin(9600);
  Serial.setTimeout(1);

  // Konfigurasi LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  // Konfigurasi Servo
  servo.attach(SERVO_PIN, 500, 2400);
  servo.write(0);
}

void loop() {
  // Kalau bukan dari serial, skip
  if (Serial.available() == 0) return;

  // Panggil serialnya di sini
  switch (Serial.readString().toInt()) {
    case 0: animateServo(5, 500); break;
    case 1: animateServo(1, 5000); break; 
  }
}
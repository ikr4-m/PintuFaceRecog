#include <Servo.h>

// Konfigurasi Servo
const uint8_t SERVO_PIN = D0;
Servo servo;

bool getFromSerial(int data) {
  return Serial.available() > 0 && Serial.readString().toInt() == data;
}

void animateServo(int count, long delayMs, bool is90Degree = true) {
  if (count < 1) return;
  for (int i = 0; i < count; i++) {
    if (i != 0) delay(delayMs);
    servo.write(0);
    delay(delayMs);
    servo.write(is90Degree ? 90 : 180);
  }
}

void setup() {
  // Buka serial pembacaan data ke komputer
  Serial.begin(9600);
  Serial.setTimeout(1);
  Serial.println(F("Receiving handshake."));

  // Konfigurasi LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  // Konfigurasi Servo
  servo.attach(SERVO_PIN, 500, 2400);
  servo.write(90);
}

void loop() {
  // Handshake untuk arduino
  if (getFromSerial(0)) animateServo(1, 500);
}
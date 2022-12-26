void animateServo(int count, long delayMs, bool is90Degree = true) {
  if (count < 1) return;
  for (int i = 0; i < count; i++) {
    if (i != 0) delay(delayMs);
    servo.write(is90Degree ? 90 : 180);
    delay(delayMs);
    servo.write(0);
  }
}

void animateBuzzer(int count, long delayMs) {
  if (count < 1) return;
  for (int i = 0; i < count; i++) {
    if (i != 0) delay(delayMs);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(delayMs);
    digitalWrite(BUZZER_PIN, LOW);
  }
}

void unlockDoor() {
  animateBuzzer(1, 250);
  animateServo(1, 5000);
}

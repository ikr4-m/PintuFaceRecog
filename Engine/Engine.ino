void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {
  if (Serial.available() == 0) return;
  bool x = Serial.readString().toInt() == 1;
  if (x) {
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
    digitalWrite(LED_BUILTIN, HIGH);
  }
}
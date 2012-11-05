bool led = 0;

void setup() {
  pinMode(11, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(A1);
  Serial.println(sensorValue);
  digitalWrite(11, led = !led);
  delay(500);
}

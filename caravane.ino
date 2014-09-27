bool led = 0;
float oldValue = 0;
const float COEF = 0.9;

void setup() {
  pinMode(11, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  float sensorValue = analogRead(A1);
  sensorValue = sensorValue * COEF + oldValue * (1-COEF);

  Serial.println(int(sensorValue));
  oldValue = sensorValue;

  digitalWrite(11, led = !led);
  delay(300);
}

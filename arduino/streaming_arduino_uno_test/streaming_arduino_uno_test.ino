void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  double now = millis()/1000;
  double a = sin(now);
  a*=100;

  double b = cos(now);
  b*=100;
  int torque1 = map(round(a), -100, 100, 0, 100);
  int torque2 = map(round(b), -100, 100, 0, 100);
  // put your main code here, to run repeatedly:
  char n[100];
  sprintf(n,"%d,%d\n",now,torque2);
  Serial.print(n);
  delay(5);
}

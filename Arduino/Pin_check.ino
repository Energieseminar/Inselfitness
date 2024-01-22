





void setup() {
  // put your setup code here, to run once:
Serial.begin (9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print(F("Messdaten Pin 2 - 14: "));
  Serial.println();
  int reading2 = analogRead(2);
  Serial.print(F("(2) : "));
  Serial.println(reading2);
  int reading3 = analogRead(3);
  Serial.print(F("(3) : "));
  Serial.println(reading3);
  int reading4 = analogRead(4);
  Serial.print(F("(4) : "));
  Serial.println(reading4);
  int reading5 = analogRead(5);
  Serial.print(F("(5) : "));
  Serial.println(reading5);

  int reading7 = analogRead(7);
  Serial.print(F("(7) : "));
  Serial.println(reading7);
  int reading8 = analogRead(8);
  Serial.print(F("(8) : "));
  Serial.println(reading8);
  int reading9 = analogRead(9);
  Serial.print(F("(9) : "));
  Serial.println(reading9);
  int reading10 = analogRead(10);
  Serial.print(F("(10) : "));
  Serial.println(reading10);
  int reading11 = analogRead(11);
  Serial.print(F("(11) : "));
  Serial.println(reading11);
  int reading12 = analogRead(12);
  Serial.print(F("(12) : "));
  Serial.println(reading12);
  int reading13 = analogRead(13);
  Serial.print(F("(13) : "));
  Serial.println(reading13);

  delay (10000);
}

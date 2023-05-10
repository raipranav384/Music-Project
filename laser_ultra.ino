int ldr1 = 13;
int value1 = 10;

int ldr2 = 12;
int value2 = 10;

int ldr3 = 11;
int value3 = 10;

int ldr4 = 10;
int value4 = 10;

const int trigPin1 = 9;
const int echoPin1 = 8;

const int trigPin2 = 7;
const int echoPin2 = 6;

void setup() {
  Serial.begin(115200);
  pinMode(ldr1, INPUT);
  pinMode(ldr2, INPUT);
  pinMode(ldr3, INPUT);
  pinMode(ldr4, INPUT);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  value1 = digitalRead(ldr1);
  value2 = digitalRead(ldr2);
  value3 = digitalRead(ldr3);
  value4 = digitalRead(ldr4);

  long duration1, distance1;
  digitalWrite(trigPin1, LOW); // Ensure the trigger pin is low
  delayMicroseconds(2);

  digitalWrite(trigPin1, HIGH); // Send a 10 microsecond pulse to the trigger pin
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);

  duration1 = pulseIn(echoPin1, HIGH); // Measure the duration of the echo pulse
  distance1 = duration1 / 58.2; // Convert duration to distance in cm

  long duration2, distance2;
  digitalWrite(trigPin2, LOW); // Ensure the trigger pin is low
  delayMicroseconds(2);

  digitalWrite(trigPin2, HIGH); // Send a 10 microsecond pulse to the trigger pin
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);

  duration2 = pulseIn(echoPin2, HIGH); // Measure the duration of the echo pulse
  distance2 = duration2 / 58.2; // Convert duration to distance in cm

  Serial.print(distance1);
  Serial.print(" ");
  Serial.print(distance2);
  Serial.print(" ");
  Serial.print(value1);
  Serial.print(" ");
  Serial.print(value2);
  Serial.print(" ");
  Serial.print(value3);
  Serial.print(" ");
  Serial.println(value4);
  delay(50);
}

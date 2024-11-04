#include <Servo.h>

// Ultrasonic Sensor Pins
const int trigPin = 10;
const int echoPin = 11;

// Variables for duration and distance
long duration;
int distance;

Servo myServo;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  myServo.attach(12);
}

void loop() {
  // Rotates the servo motor from 15 to 165 degrees
  for (int i = 15; i <= 165; i++) {  
    myServo.write(i);
    delay(30);
    distance = calculateDistance(); // Calculates distance

    // Send angle and distance to Serial
    Serial.print(i);
    Serial.print(",");
    Serial.print(distance);
    Serial.print(".");
    Serial.println(); // Adds newline for better readability

    // Print distance for debugging
    Serial.println(distance);
  }

  // Rotates servo back from 165 to 15 degrees
  for (int i = 165; i > 15; i--) {  
    myServo.write(i);
    delay(30);
    distance = calculateDistance();

    Serial.print(i);
    Serial.print(",");
    Serial.print(distance);
    Serial.print(".");
    Serial.println(); // Adds newline for better readability

    // Print distance for debugging
    Serial.println(distance);
  }
}

int calculateDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
}

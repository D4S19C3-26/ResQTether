/*
 * ResQTether ESP32 Motor Controller
 * Protocol: "V,<linear_x>,<angular_z>\n"
 * Example:  "V,0.50,0.00\n" (Forward)
 *           "V,-0.50,0.00\n" (Reverse)
 *           "V,0.00,1.00\n" (Turn Left)
 *           "V,0.00,-1.00\n" (Turn Right)
 * 
 * Hardware:
 *   ESP32 Dev Module
 *   L298N Dual H-Bridge Motor Driver
 *   4x TT DC Gear Motors (Left pair parallel, Right pair parallel)
 * 
 * Pinout:
 *   IN1 -> GPIO 25 (Left Forward)
 *   IN2 -> GPIO 26 (Left Reverse)
 *   IN3 -> GPIO 27 (Right Forward)
 *   IN4 -> GPIO 14 (Right Reverse)
 *   ENA -> 5V Jumper ON (or GPIO 32 if PWM speed control needed)
 *   ENB -> 5V Jumper ON (or GPIO 33 if PWM speed control needed)
 */

#define IN1 25
#define IN2 26
#define IN3 27
#define IN4 14

unsigned long last_cmd_time = 0;
const unsigned long TIMEOUT_MS = 1000; // Stop if no ROS command received within 1 sec

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void moveBackward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void turnLeft() {
  // Pivot left: Left motors backward, Right motors forward
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void turnRight() {
  // Pivot right: Left motors forward, Right motors backward
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void setup() {
  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopMotors();
  Serial.println("ESP32_MOTOR_READY");
}

void loop() {
  // Check for incoming serial command from Jetson / Laptop ROS 2 bridge
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line.startsWith("V,")) {
      int firstComma = line.indexOf(',');
      int secondComma = line.indexOf(',', firstComma + 1);

      if (firstComma > 0 && secondComma > firstComma) {
        float linear = line.substring(firstComma + 1, secondComma).toFloat();
        float angular = line.substring(secondComma + 1).toFloat();

        last_cmd_time = millis();

        // Differential steering logic
        if (linear > 0.1) {
          if (angular > 0.2) {
            turnLeft();
          } else if (angular < -0.2) {
            turnRight();
          } else {
            moveForward();
          }
        } else if (linear < -0.1) {
          moveBackward();
        } else if (angular > 0.15) {
          turnLeft();
        } else if (angular < -0.15) {
          turnRight();
        } else {
          stopMotors();
        }
      }
    }
  }

  // Safety Watchdog: Stop motors if serial commands cease
  if (millis() - last_cmd_time > TIMEOUT_MS) {
    stopMotors();
  }
}

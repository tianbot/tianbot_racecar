#include <Servo.h>

#define    STX          0x02
#define    ETX          0x03

Servo myservo;
int servo_val = 90;     //120左  90中点  60右

Servo mymotor;
int motor_val = 1500;     //1800前进  1500中点  1200倒退
byte cmd[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};                 // bytes received

void setup() {
  Serial.begin(57600);
  myservo.attach(3);
  mymotor.attach(9);
  myservo.write(servo_val);
  mymotor.write(motor_val);
}

void loop() {
  if (Serial.available())  {                          // data received from smartphone
    delay(2);
    cmd[0] =  Serial.read();
    if (cmd[0] == STX)  {
      int i = 1;
      while (Serial.available())  {
        delay(1);
        cmd[i] = Serial.read();
        if (cmd[i] > 127 || i > 8)                 break; // Communication error
        if ((cmd[i] == ETX) && (i == 8))           break; // Button or Joystick data
        i++;
      }
      if     (i == 8)          sendCmd(cmd);  // 3 Bytes  ex: < STX "C" ETX >
    }
  }
}

void sendCmd(byte data[8])    {
  int motor_val = data[1] * 1000 + data[2] * 100 + data[3] * 10 + data[4]; // obtain the Int from the ASCII representation
  int servo_val = data[5] * 100 + data[6] * 10 + data[7];
  if (motor_val < 1200)
  {
    motor_val = 1200;
  }
  if (motor_val > 1800)
  {
    motor_val = 1800;
  }
  mymotor.writeMicroseconds(motor_val);
  if (servo_val < 60)
  {
    servo_val = 60;
  }
  if (servo_val > 120)
  {
    servo_val = 120;
  }
  myservo.write(servo_val);
}


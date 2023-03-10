#include <ros.h>
#include <std_msgs/Float32.h>

ros::NodeHandle nh;

const int In1 = 2; // Analog output pin 
const int In2 = 3; // Analog output pin 
const int EnA = 11; // Activar o desactivar Puente H

const int Vcc = 5;
const int Vcc_sc = Vcc/255;

float voltage,duty;
int pwm = 0;

float sgn_ros;

void direction_fcn(const std_msgs::Float32& msg)
{
  sgn_ros = msg.data;
  Serial.println("DR");
  digitalWrite(In1, sgn_ros>0.01);
  digitalWrite(In2, sgn_ros<0.01);
  pulse();
}

ros::Subscriber<std_msgs::Float32> sub("cmd_pwm", direction_fcn);

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(EnA, OUTPUT); 
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT); 

  nh.initNode();
  nh.subscribe(sub);
}

void loop() { nh.spinOnce(); delay(1); }

void pulse ()
{
  pwm = abs(sgn_ros*255);
  voltage = pwm * Vcc_sc;
  duty = 100*voltage/Vcc;
  
  analogWrite(EnA, pwm);
  print_data();
}

void print_data()
{
  Serial.print("EL ciclo de trabajo del pwm es:  ");
  Serial.print(duty);
  Serial.print("  %");
  Serial.print("    EL cual corresponde a:  " );
  Serial.print(voltage);
  Serial.println("  Volts" );
}

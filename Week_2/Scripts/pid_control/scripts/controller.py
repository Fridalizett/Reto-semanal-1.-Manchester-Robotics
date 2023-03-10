#!/usr/bin/env python
#from typing import Self

#Este codigo fue complementado y tomando de esqueleto al codigo
# realizado en las clases de Control y Actuadores con el arduino
import rospy
import numpy as np
from pid_control.msg import motor_output
from pid_control.msg import motor_input
from pid_control.msg import set_point


#Setup parameters, variables and callback functions here (if required)

#Definicion de las variables en motor_input.msg
input = motor_input()
input.input = 0.0
input.time = 0.0

#Parametros de control_params.yaml para diferentes valores de entrada
VMotor = rospy.get_param("sp", 0.0)
VMotor1 = rospy.get_param("sp1", 5.0)
VMotor2 = rospy.get_param("sp2", 1.0)
VMotor3 = rospy.get_param("sp3", 8.0)
VMotor4 = rospy.get_param("sp4", 3.0)
VMotor5 = rospy.get_param("sp5", 7.0)
VMotor6 = rospy.get_param("sp6", 7.0)

#Diferentes valores de kp, ki, kd para ver el desempeno del controlador 
kp = rospy.get_param("kp", 2.0)

ki = rospy.get_param("ki", 6.0)

#Tiempo de muestreo
Ts = rospy.get_param("TS", 0.02)

#Definicion de las variables en motor_output.msg
output = motor_output()
output.output = 0.0
output.time = 0.0
output.status = ""


#Calculo de constantes del controlador PID con diferentes situaciones(subamortiguado, criticamente,sobreamortiguado)
K1 = kp + Ts*ki

u = [0.0, 0.0]        #U es la Matriz de salida del controlador 
e = [0.0, 0.0, 0.0]   #E es la Matriz de error del sistema controlado

#Funcion para definir las variables de salida
def callback(msg) :
  global output 
  output = msg

def callbacksp(msgsp):
  global set_sp
  set_sp = msgsp.outsp

#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")

if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("controller")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)

    #Setup Publishers and subscribers here
    pub = rospy.Publisher("/motor_input", motor_input, queue_size = 1)
    rospy.Subscriber("/motor_output", motor_output, callback)

    rospy.Subscriber("/set_point", set_point, callbacksp)

    print("The Controller is Running")
    #Run the node
    while not rospy.is_shutdown():
        #Write your code here

        #Se muestran las posibles diferentes situaciones(subamortiguado, sobreamortiguado y criticamente amortiguado)
        #Para ello se hizo variar los valores de kp,ki, kd y el voltaje de entrada
        if (output.time < 10):
          e[0] = VMotor - output.output
        if(output.time > 10.1):
          e[0] = VMotor1 - output.output
        if(output.time > 15):
          e[0] = VMotor2 - output.output

          kp
          ki
          
          Ts

          K1 = kp + Ts*ki
          
        if(output.time > 25):
          e[0] = VMotor3 - output.output

          kp
          ki
          Ts

          K1 = kp + Ts*ki
          
        if(output.time > 35):
          e[0] = VMotor4 - output.output

          kp
          ki
          Ts

          K1 = kp + Ts*ki
        #En esta condicion se deja el controlador mal entonado, y en la grafica se ve como queda oscilando
        if(output.time > 45):
          e[0] = VMotor5 - output.output

          kp
          ki
          
          Ts

          K1 = kp + Ts*ki
             
        if(output.time > 55):
          e[0] = VMotor6 - output.output

          kp
          ki
          
          Ts

          K1 = kp + Ts*ki
        

        u[0] = K1*e[0] + K1*e[1] + K1*e[2] + u[1]
        e[2] = e[1]
        e[1] = e[0]
        u[1] = u[0]

        input.input = u[0] * (1.0 / 13.0)

        pub.publish(input)
        print(output.output)

        rate.sleep()
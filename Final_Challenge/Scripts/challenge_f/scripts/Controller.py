#!/usr/bin/env python
import rospy 
import numpy as np
from challenge_f.msg import motor_output
from challenge_f.msg import set_point
from challenge_f.msg import motor_input
from std_msgs.msg import Float32
from std_msgs.msg import Float64

#Aqui generamos el topic de /motor_input (publish)(debe ir de [1 -1]) y 
# motor_output y set_point (suscribers)
#debe de incluir un archivo de parametros 
k=13.2
t_tau=0.04
sistema=0
#inicializamos las varibales de control 
kp = rospy.get_param("kp",0.57) 
ki = rospy.get_param("ki",0.56)
kd = rospy.get_param("kd",0.115)
Ts = rospy.get_param("Ts",0.02) 
tau = rospy.get_param("tau",0.0275) 
R_1 = rospy.get_param("R",0.14) 
dt = rospy.get_param("dt",0.11) 
signal_data = 0.0
time_data = 0.0
error = 0.0
error_acumulado=0.0
error_res=0.0
error_an=0.0
error_anterior=0.0
ultima_medicion = 0.0
angularVelocity = 0.0 #??
cv1=0
signal2=0

#inicializamos el archivo del motor
#output = motor_output()
#output.output = 0.0
#output.time = 0.0

input = motor_input()
input.input = 0.0
input.time = 0.0

out_motor=0
#mandamos a llamar a los mensajes 
def callback(msg):
    global signal_data, time_data
    signal_data = msg.signal_y
    time_data = msg.time_x 
#esta no la entiendo 

def callback2(msgsignal):
    global out_motor
    out_motor = msgsignal.data


#Creamos la funcion stop para cuando paremos el codigo
def stop(self):
    pub.publish(0)
    rate.sleep()
    print("stopping")

#Empezamos a estructurar nuestro nodo 
if __name__=='__main__':
    rospy.init_node("Controller")
    #Revisar si tenemos que modificar este rate? es el rate de transmicion me imagino
    rate= rospy.Rate(10) #frecuencia en hz
   
    #Cuando se apaga encendemos la funcion stop
    rospy.on_shutdown(stop)

    #Publicamos y suscribimos los topic de nuestro nodo 
    #este debe de ser un custum message
    rospy.Subscriber("set_point", set_point,callback)
    rospy.Subscriber("motor_output", Float32,callback2)
    pub=rospy.Publisher("motor_input", Float32,queue_size=10)
    print("The motorn_input is running")
    t0= rospy.Time.now().to_sec()
    while not rospy.is_shutdown():
        #calculamos el error comparando la signal de entrada con la retroalimentada
        #el set_point menos la signal de salida del motor
        #expo=
        #sistema=k/(t_tau+1)
        error=signal_data-out_motor
        error_acumulado= error*dt 
        error_res =(error - error_anterior)/ dt
        proporcional= kp*error
        integral= ki*error_acumulado
        derivativo= kd*error_res
        cv= proporcional+integral+derivativo+(1.6*signal_data)
        u=cv*R_1
        velocidad = ultima_medicion + ((u - ultima_medicion))
        ultima_medicion = velocidad
        signal2=ultima_medicion
        signal=ultima_medicion
        if signal_data==0:
            error=0
        error_anterior = error
        #Realizamos la operacion del control 
        #signal2=signal_data
        #cargamos la informacion al nodo y publicamos
        rospy.loginfo(out_motor)
        pub.publish(signal)
        rate.sleep()

        #rospy.loginfo(output.output)
        #pub.publish(output.output)     
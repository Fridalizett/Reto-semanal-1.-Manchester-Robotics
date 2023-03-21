#!/usr/bin/env python
import rospy 
import numpy as np
from challenge_f.msg import set_point
from std_msgs.msg import Float32

tipo= 3

#inicializa el archivo set_point
msg = set_point()
msg.time_x = 0.0
msg.signal_y = 0.0

#Aqui va el tipo=

#Creamos la funcion stop para cuando paremos el codigo
def stop(self):
    pub_signal.publish(0)
    pub_motor.publish(0)
    rate.sleep()
    print("stopping")

#Empezamos a estructurar nuestro nodo 
if __name__=='__main__':
    rospy.init_node("Input")
    #Revisar si tenemos que modificar este rate? es el rate de transmicion me imagino
    rate= rospy.Rate(10)
   
    #Cuando se apaga encendemos la funcion stop
    rospy.on_shutdown(stop)

    #Publicamos el topic de nuestro nodo
    # porque se ponen dos? 
    pub_signal = rospy.Publisher("set_point", set_point,queue_size=10)
    pub_motor=rospy.Publisher("signal",Float32, queue_size=10)
    print("The set point generator is running")
    t0= rospy.Time.now().to_sec()
    
    #planteamos la logica de nuestro programa y corremos el nodo
    while not rospy.is_shutdown():
        tipo=rospy.get_param("tipo",3)
        #estructura del seno 
        if tipo== 1:
            P=rospy.get_param("P",21)
            phase= rospy.get_param("phase",0)
            amplitud= rospy.get_param("amplitud",0.5)
            offset= rospy.get_param("offset",0)
            w=2*np.pi/P
            t= rospy.Time.now().to_sec()-t0
            timeset=t
            setout=(np.sin(w*t+phase)*amplitud)+offset
        
        #estructura del square
        elif tipo==2:
            P=rospy.get_param("P",10)
            phase= rospy.get_param("phase",0)
            amplitud= rospy.get_param("amplitud",1)
            offset= rospy.get_param("offset",0)
            w=2*np.pi/P
            t= rospy.Time.now().to_sec()-t0
            if(np.sin(w*t+phase)*amplitud)>=0:
                setout=rospy.get_param("tope",1)
                timeset=t
            else:
                setout=rospy.get_param("fondo",0)
                timeset=t
        
        #estructura del step 
        elif tipo==3:
            P=rospy.get_param("P",21)
            phase= rospy.get_param("phase",0)
            amplitud= rospy.get_param("amplitud",1)
            offset= rospy.get_param("offset",1)
            #w=2*np.pi/P
            #Aqui modifico el offset para que se mueva 
            t= rospy.Time.now().to_sec()-t0
            setout=offset
            timeset=t

        #publicar
        #estas lineas para que son????
        msg.time_x = timeset
        msg.signal_y = setout
        #-------
        pub_signal.publish(msg)
        rospy.loginfo(setout)
        pub_motor.publish(setout)  
        
        rate.sleep()              


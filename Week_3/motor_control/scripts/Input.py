#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32
tipo =3

def stop(self):
    pub.publish(0)
    rate.sleep()
    print("stopping")

if __name__=='__main__':
    rospy.init_node("Input")
    rate= rospy.Rate(30)
    rospy.on_shutdown(stop)
    pub = rospy.Publisher("cmd_pwm", Float32,queue_size=10)
    print("The set point generator is running")
    t0= rospy.Time.now().to_sec()

    #Run Node
    while not rospy.is_shutdown():
        tipo=rospy.get_param("tipo",2)
        if tipo== 2:
            P=rospy.get_param("P",21)
            phase= rospy.get_param("phase",0)
            amplitud= rospy.get_param("amplitud",1)
            offset= rospy.get_param("offset",0)
            w=2*np.pi/P
            t= rospy.Time.now().to_sec()-t0
            timeset=t
            setout=(np.sin(w*t+phase)*amplitud)+offset
        elif tipo==3:
            P=rospy.get_param("P",21)
            phase= rospy.get_param("phase",0)
            amplitud= rospy.get_param("amplitud",1)
            offset= rospy.get_param("offset",0)
            w=2*np.pi/P
            t= rospy.Time.now().to_sec()-t0
            if(np.sin(w*t+phase)*amplitud)>=0:
                setout=rospy.get_param("tope",1)
                timeset=t
            else:
                setout=rospy.get_param("fondo",-1)
                timeset=t

        #publicar
        rospy.loginfo(setout)
        pub.publish(setout)                
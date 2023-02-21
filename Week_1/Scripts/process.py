#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32
          
o_signal = 0
o_time = 0

def callbacksignal(msgsignal):
    global o_signal
    o_signal = msgsignal.data

def callbacktime(msgtime):
    global o_time
    o_time = msgtime.data

if __name__=='__main__':
    rospy.init_node('process')
    rospy.Subscriber("signal", Float32, callbacksignal)
    rospy.Subscriber("time", Float32, callbacktime)

    pub_signal2 = rospy.Publisher("process_2", Float32, queue_size = 10)
    pub_time = rospy.Publisher("time_2", Float32, queue_size = 10)
    rate = rospy.Rate(10) #10 Hz

    while not rospy.is_shutdown():
        t=o_time

        des_sign=((o_signal * np.cos(5)) + np.cos(t) * np.sin(5))*-np.cos(t)
        resultado = "%3f | %3f" %(des_sign,t)
        rospy.loginfo(resultado)
        pub_signal2.publish(des_sign)
        pub_time.publish(t)

        rate.sleep()
#!/usr/bin/env python
import numpy as np
import rospy
from std_msgs.msg import Float32
if __name__=='__main__':
    rospy.init_node("signal_generator")
    pub_signal=rospy.Publisher("signal", Float32, queue_size=10)
    pub_time=rospy.Publisher("time", Float32, queue_size=10)
    rate=rospy.Rate(10)
    time= 0
    while not rospy.is_shutdown():
        time+=0.1
        signal= np.sin(time)
        result = "%3f | %3f" %(signal,time)
        rospy.loginfo(result)
        pub_signal.publish(signal)
        pub_time.publish(time)
        rate.sleep()
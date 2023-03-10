#!/usr/bin/env python
import rospy
import numpy as np
from pid_control.msg import set_point

# Setup Variables, parameters and messages to be used (if required)


#Stop Condition
def stop():
 #Setup the stop message (can be the same as the control message)
  print("Stopping")


if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("Set_Point_Generator")
    rate = rospy.Rate(100)
    rospy.on_shutdown(stop)

    #Setup Publishers and subscribers here
    pub = rospy.Publisher("/set_point", set_point, queue_size = 1)


    print("The Set Point Genertor is Running")

    #Run the node
    while not rospy.is_shutdown():

        #Write your code here
        sp = rospy.get_param("sp", 8.0)

        sp_output = set_point()
        sp_output.outsp = sp

        rospy.loginfo(sp_output)
        #pub.publish(sp_output)

        rate.sleep()
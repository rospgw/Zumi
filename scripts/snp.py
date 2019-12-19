#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32

def talk():
    msg = (150 - (ye + bl)/2)*0.5
    print(msg)
    pub = rospy.Publisher('pimsg', Float32, queue_size=10)
    #rospy.init_node('pi', anonymous=True)
    #rate = rospy.Rate(10)
    #msg = data.data
    #rospy.loginfo(msg)
    pub.publish(msg)
    #rate.sleep()

def callback_y(data):
    rospy.loginfo('yellow %f', data.data)
    global ye
    ye = data.data
    talk()

def callback_b(data):
    rospy.loginfo('black %f', data.data)
    global bl
    bl = data.data
    talk()

def listener():

    rospy.init_node('pi', anonymous=True)

    rospy.Subscriber('yellow', Float32, callback_y)
    rospy.Subscriber('black', Float32, callback_b)

    rospy.spin()

if __name__ == '__main__':
    listener()
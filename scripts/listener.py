#!/usr/bin/env python

import rospy
from std_msgs.msg import Int64

def callback(data):
    rospy.loginfo('pi %s', data.data)

def listener():

    rospy.init_node('pilisten', anonymous=True)

    rospy.Subscriber('pimsg', Int64, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()

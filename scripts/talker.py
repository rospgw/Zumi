#!/usr/bin/env python

import rospy
from std_msgs.msg import Int64

def talk():
    pub = rospy.Publisher('chatter', Int64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        msg = 1
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__ =="__main__":
	talk()
    
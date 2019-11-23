#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


def callback(img_msg):
    bridge = CvBridge()
    rospy.loginfo('hello ROS!')
    cv_image = bridge.imgmsg_to_cv2(img_msg, desired_encoding="bgr8")
    cv2.imshow('receive image',cv_image)
    cv2.waitKey(1)
def receiver():

    rospy.init_node('receiver',anonymous=True)
    rospy.Subscriber('image_topic',Image,callback)
    rospy.spin()

if __name__ == '__main__':
    receiver()    
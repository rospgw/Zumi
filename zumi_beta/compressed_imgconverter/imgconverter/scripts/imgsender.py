#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


def sender():
    pub = rospy.Publisher('image_topic',Image,queue_size=1)
    rospy.init_node('sender',anonymous=True)
    rate = rospy.Rate(60)
    
    cap = cv2.VideoCapture(0)
    bridge = CvBridge()

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")

        if ret:
            rospy.loginfo("capturing image success!")
    
        pub.publish(msg)
        rate.sleep()

if __name__== '__main__':
    try:
        sender()
    except rospy.ROSInterruptException:
        pass
        
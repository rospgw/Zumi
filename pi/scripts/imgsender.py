#!/usr/bin/env python

import rospy
import cv2
import os
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

os.system('sudo modprobe bcm2835-v4l2')

def sender():
	pub = rospy.Publisher('image_topic', Image, queue_size=10)
	rospy.init_node('sender', anonymous=True)
	rate = rospy.Rate(30)

	cap = cv2.VideoCapture(-1)
	bridge = CvBridge()
	if cap.isOpened():
		rospy.loginfo('capturing image success')
	while not rospy.is_shutdown():
		ret, frame = cap.read()
		frame = cv2.resize(frame, (100,100))

		msg = bridge.cv2_to_imgsmg(frame, encoding="passthrough")
		pub.publish(msg)
		rate.sleep()

if __name__ == '__main__':
	try:
		sender()
	except rospy.ROSInterruptException:
		pass
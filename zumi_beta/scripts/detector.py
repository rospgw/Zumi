#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from std_msgs.msg import Float32
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np


def callback(img_msg):
    flag = 0
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(img_msg, desired_encoding="passthrough")
    flip_cv_image = cv2.flip(cv_image,-1)
    frame = cv2.resize(flip_cv_image,(300,300))
    frame_p = frame
    frame = frame[220:300,0:300]
     
    frame_hsv_y = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_hsv_p = cv2.cvtColor(frame_p, cv2.COLOR_BGR2HSV)
    
    # lower_color_y= (0,72,0)
    # upper_color_y=(53,255,255)
    lower_color_y= (0,52,190)
    upper_color_y=(52,177,255)

    lower_color_p= (105,59,106)
    upper_color_p=(132,106,190)

    frame_mask_y = cv2.inRange(frame_hsv_y,lower_color_y,upper_color_y)
    frame_mask_p = cv2.inRange(frame_hsv_p,lower_color_p,upper_color_p)
    
    kernel = np.ones((5, 5), np.uint8)
    
    frame_mask_y = cv2.erode(frame_mask_y, kernel, iterations=1)
    frame_mask_y = cv2.dilate(frame_mask_y, kernel, iterations=1)
    frame_mask_y = cv2.GaussianBlur(frame_mask_y, (3, 3), 0)

    frame_mask_p = cv2.erode(frame_mask_p, kernel, iterations=1)
    frame_mask_p = cv2.dilate(frame_mask_p, kernel, iterations=1)
    frame_mask_p = cv2.GaussianBlur(frame_mask_p, (3, 3), 0)

    _,contours_p, hierarchy = cv2.findContours(frame_mask_p, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours_p) >0:
        areas_p = [cv2.contourArea(c) for c in contours_p]
        max_index_p = np.argmax(areas_p)
        cnt_p = contours_p[max_index_p]
        cv2.drawContours(frame_p, cnt_p, -1, (255, 0, 0), 5)
        
        flag=1
    else:
        flag=0

    if flag ==1:
        pub_yellow.publish(255)###
        print 1000

    if flag ==0:

        _,contours_y, hierarchy = cv2.findContours(frame_mask_y, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours_y)==0:
        	pub_yellow.publish(100)
			
        areas_y = [cv2.contourArea(c) for c in contours_y]
        max_index_y = np.argmax(areas_y)
        cnt_y = contours_y[max_index_y]
        cv2.drawContours(frame, cnt_y, -1, (255, 0, 0), 5)

        M_y = cv2.moments(cnt_y)
        cx_y = int(M_y['m10']/M_y['m00'])
        cy_y = int(M_y['m01']/M_y['m00'])
        cv2.circle(frame, (cx_y, cy_y), 5, (0,255,255), -1)
        cx_y= (40 - cx_y)*0.03;
        if (cx_y<0):
            cx_y=-cx_y+10
        pub_yellow.publish(cx_y)###
    	print cx_y
    cv2.imshow('purple',frame_p)
    cv2.imshow('frame',frame)
    cv2.waitKey(1)
#def receiver():

    
if __name__ == '__main__':
    rospy.init_node('receiver',anonymous=True)

    pub_yellow=rospy.Publisher('yellow_x',Float32, queue_size=10)   ####

    rospy.Subscriber('image_topic',Image,callback)
    rospy.spin()


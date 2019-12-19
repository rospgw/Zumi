#!/usr/bin/env python
import rospy
import cv2
from std_msgs.msg import String
from std_msgs.msg import Float32
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import numpy as np
import pytesseract
import Queue
import tensorflow as tf

callback_queue = Queue.Queue()
graph = tf.get_default_graph()

def order_points(pts):
    rect = np.zeros((4,2),dtype = 'float32')
    rect_list = []
    for a in range(0,8):
        rect_list.append(pts[a][0])
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    rect[1]= pts[rect_list.index(max(rect_list))]
    rect[3]= pts[rect_list.index(min(rect_list))]
    return rect

def prediction_callback(img):
    global count_t
    text = pytesseract.image_to_string(img)
    return text

def callback(img_msg):
    global blank
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(img_msg, desired_encoding="passthrough")
    flip_cv_image = cv2.flip(cv_image,-1)
    # frame2 = cv2.resize(flip_cv_image,(320,240))
    blank = 255 * np.ones(shape=[300, 300, 3], dtype=np.uint8)
    frame2 = flip_cv_image
    orig = frame2.copy()
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(frame2, 75, 200)
    global graph
    _, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        area = cv2.contourArea(approx)
        
        if len(approx) == 8:
            screenCnt = approx
            area = cv2.contourArea(screenCnt)
            if area>500:
                cv2.drawContours(orig, [screenCnt], -1, (0, 255, 0), 2)
                
                rect = order_points(screenCnt.reshape(8, 2))  # /2)
                (topLeft, topRight, bottomRight, bottomLeft) = rect

                w1 = abs(bottomRight[0] - bottomLeft[0])
                w2 = abs(topRight[0] - topLeft[0])
                h1 = abs(topRight[1] - bottomRight[1])
                h2 = abs(topLeft[1] - bottomLeft[1])

                maxWidth = max([w1, w2])
                maxHeight = max([h1, h2])
                
                dst = np.float32([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]])

                M = cv2.getPerspectiveTransform(rect, dst)
                warped = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))
                warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
                warped = cv2.adaptiveThreshold(warped, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 0)
                
                kernel = np.ones((3, 3), np.uint8)
                warped = cv2.cvtColor(warped, cv2.COLOR_GRAY2BGR)
                if warped.shape[1]<500: 
                    blank[100:100 + warped.shape[0], 100:100 + warped.shape[1]] = warped
                

            
                    
                with graph.as_default():      
                    callback_queue.put(lambda: prediction_callback(blank))
                
                cv2.imshow('ba',blank)

                # text = pytesseract.image_to_string(blank)
            # if text.find("t")==-1 :
            #     blank = 255 * np.ones(shape=[1000, 1000, 3], dtype=np.uint8)
            #     matrix = cv2.getRotationMatrix2D((warped.shape[1] / 2, warped.shape[0] / 2), -43, 1)
            #     warped = cv2.warpAffine(warped, matrix, (warped.shape[1], warped.shape[0]))

            #     blank[100:100 + warped.shape[0], 100:100 + warped.shape[1]] = warped
            #     text = pytesseract.image_to_string(blank)
    
    cv2.imshow('d',orig)
    cv2.waitKey(1)
    
if __name__ == '__main__':
    global count_t
    rospy.init_node('img_receiver',anonymous=True)
    
    rospy.Subscriber('image_topic',Image,callback)
    pub = rospy.Publisher('stop',Float32, queue_size=10)
    while not rospy.is_shutdown():
        try:
            prediction = callback_queue.get(True, 2)()
            if prediction != '':
                pub.publish(200)
                print prediction
            else:
                pub.publish(0)
                count = 0
            
          
        except Queue.Empty:
            print "here"
            pass
    blank = 255 * np.ones(shape=[300, 300, 3], dtype=np.uint8)

    rospy.spin()
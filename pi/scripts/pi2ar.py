#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32, Int64
import smbus
import time
import math

def callback_y(data):
	global ye
	ye = data.data
	rospy.loginfo('yellow %d', ye)
	i2c.run()

def callback_s(data):
	global st
	st = data.data
	rospy.loginfo('stop %d', st)
	i2c.run()

def listener():
	rospy.init_node('pi', anonymous=True)
	rospy.Subscriber('yellow_x', Float32, callback_y)
	rospy.Subscriber('stop', Float32, callback_s)
	rospy.spin()

class I2CComm(object):
	I2C_BUS_NUM = 1

	def __init__(self):
		self.master = smbus.SMBus(self.I2C_BUS_NUM)
		self.slave_addr_list = [4]

	def run(self):
		me = self.master

		for addr in self.slave_addr_list:
			try:
				if st==200:
					me.write_byte(addr, int(st))
				else:
					me.write_byte(addr, int(ye))
			except IOError:
				pass

if __name__ == '__main__':
	st=0
	
	i2c = I2CComm()
	listener()

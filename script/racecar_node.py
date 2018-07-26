#!/usr/bin/env python
import rospy
import serial
import time
from geometry_msgs.msg import Twist

port = rospy.get_param("~port", "/dev/racecar")
baud = int(rospy.get_param("~baud", 57600))

t = serial.Serial(port, baud, timeout=0.5)

def callback(data):

	gas = int(data.linear.x)
        gas = str(gas)

	angle = int(data.angular.z)
	if angle  >= 100:
		angle=str(angle)
	else :
		angle='0'+str(angle)
	
        p = bytearray()
        p.append(2)	
        print(gas)
        [p.append(int(i)) for i in gas]	
        [p.append(int(i)) for i in angle]	
        p.append(3)	
        t.write(p)

	rospy.loginfo(gas+'-'+angle)

def speed_controller():
	rospy.init_node('racecar_node',anonymous=True)
	rospy.loginfo('start!')
	rospy.Subscriber('/car/cmd_vel', Twist, callback)
	rospy.spin()

if __name__ == '__main__':
	speed_controller()

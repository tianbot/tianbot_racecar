#!/usr/bin/env python
import rospy
import time
from  sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

twist = Twist()
joy_mode = "D"
#init speed. in case of random num
twist.linear.x = 1500
twist.angular.z = 90

def callback(data):
    #reset the speed every cycle. 
    twist.linear.x = 1500
    twist.angular.z = 90
    
    if joy_mode == "d" or joy_mode == "D":
        if data.buttons[4]==1:
            twist.linear.x = int(1500 + data.axes[1] * 500)

        if data.buttons[5]==1:
            twist.angular.z = int(90 + 30 * data.axes[2])
    elif joy_mode == "x" or joy_mode == "X":
        if data.buttons[4]==1:
            twist.linear.x = int(1500 + data.axes[1] * 500)

        if data.buttons[5]==1:
            twist.angular.z = int(90 + 30 * data.axes[3])


def joystick_controller():
    rospy.init_node('racecar_joy',anonymous=True)
    rospy.loginfo('start!')
    joy_mode = rospy.get_param("/joy_mode", "D")

    pub = rospy.Publisher('~/car/cmd_vel', Twist, queue_size=5)

    rospy.Subscriber('/joy', Joy, callback)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        pub.publish(twist)
        rate.sleep()


if __name__ == '__main__':
    joystick_controller()

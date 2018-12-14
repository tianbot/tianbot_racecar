#!/usr/bin/env python
import rospy
import time
from  sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class RacecarJoyTeleop(object):
    "Tianbot racecar joy teleop node. rewrite from cpp turtlebot logitech teleop"
    def __init__(self):
        rospy.loginfo("Tianbot Racecar JoyTeleop Initializing...")
        self._twist = Twist()
        self._twist.linear.x = 1500
        self._twist.angular.z = 90
        self._deadman_pressed = False
        self._zero_twist_published = False
       
       
        self._cmd_vel_pub = rospy.Publisher('~/car/cmd_vel', Twist, queue_size=5)
        self._joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)
        self._timer = rospy.Timer(rospy.Duration(0.05), self.joystick_controller)
        
        self._joy_mode = rospy.get_param("~joy_mode", "D") 
        if self._joy_mode == "d" or self._joy_mode == "D":
            self._axis_throttle = 1
            self._axis_servo = 2
        elif self._joy_mode == "x" or self._joy_mode == "X":
            self._axis_throttle = 1
            self._axis_servo = 3

        self._throttle_scale = rospy.get_param("~throttle_scale", 0.5)
        self._servo_scale = rospy.get_param("~servo_scale", 1)


    def joy_callback(self, joy):
        #reset the speed every cycle. 
        self._twist.linear.x = 1500
        self._twist.angular.z = 90
        if joy.buttons[4]==1:
            self._twist.linear.x = int(1500 + joy.axes[self._axis_throttle] * self._throttle_scale * 300)

        if joy.buttons[5]==1:
            self._twist.angular.z = int(90 + joy.axes[self._axis_servo] * self._servo_scale * 30)

        self._deadman_pressed = joy.buttons[4] or joy.buttons[5]


    def joystick_controller(self, tdat):
        if self._deadman_pressed:
            self._cmd_vel_pub.publish(self._twist)
            self._zero_twist_published = False
        elif not self._deadman_pressed and not self._zero_twist_published:
            self._cmd_vel_pub.publish(self._twist)
            self._zero_twist_published = True


if __name__ == '__main__':
    try:
        rospy.init_node('racecar_joy_teleop',anonymous=True)
        rjt = RacecarJoyTeleop()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.logwarn("Error in main function")

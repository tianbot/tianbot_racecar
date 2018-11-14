#!/usr/bin/env python

#Python client library for ROS
import rospy
import sys
import time
import math

#This module helps to receive values from serial port
from SerialDataGateway import SerialDataGateway
#Importing ROS data types
from std_msgs.msg import Int16,Int32, Int64, Float32, String, Header, UInt64
#Importing ROS data type for IMU
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist, Quaternion

#Class to handle serial data from TianBot_RACECAR and converted to ROS topics
class TianBot_RACECAR_Class(object):
	
	def __init__(self):
		print "Initializing TianBot_RACECAR Class"

#######################################################################################################################
		#Sensor variables
		self._Counter = 0

		self._battery_value = 0

		self._qx = 0
		self._qy = 0
		self._qz = 0
		self._qw = 0

		self._servo = 0
		self._motor = 0

		self._robot_heading = 0
#######################################################################################################################
		#Get serial port and baud rate of Tiva C TianBot_RACECAR
		port = rospy.get_param("~port", "/dev/ttyUSB0")
		baudRate = int(rospy.get_param("~baudrate", 115200))

#######################################################################################################################
		rospy.loginfo("Starting with serial port: " + port + ", baud rate: " + str(baudRate))
		#Initializing SerialDataGateway with port, baudrate and callback function to handle serial data
		self._SerialDataGateway = SerialDataGateway(port, baudRate,  self._HandleReceivedLine)
		rospy.loginfo("Started serial communication")
		

#######################################################################################################################
#Subscribers and Publishers

		#Publisher for Battery level(for upgrade purpose)
		self._Battery_Level = rospy.Publisher('battery_level',Float32,queue_size = 10)

		#Publisher for entire serial data
		self._SerialPublisher = rospy.Publisher('serial', String,queue_size=10)
		
#######################################################################################################################
#Subscribers and Publishers of IMU data topic

		self.frame_id = 'IMU_link'

	        self.cal_offset = 0.0
        	self.orientation = 0.0
        	self.cal_buffer =[]
        	self.cal_buffer_length = 1000
        	self.imu_data = Imu(header=rospy.Header(frame_id="IMU_link"))
        	self.imu_data.orientation_covariance = [0.0025,0,0,0,0.0025,0,0,0,0.0025]
	        self.imu_data.angular_velocity_covariance = [0.02,0,0,0,0.02,0,0,0,0.02]
        	self.imu_data.linear_acceleration_covariance = [0.04,0,0,0,0.04,0,0,0,0.04]
        	self.gyro_measurement_range = 300.0 
        	self.gyro_scale_correction = 1.35
        	self.imu_pub = rospy.Publisher('imu_data', Imu,queue_size = 10)

		self.deltat = 0
		self.lastUpdate = 0

#New addon for computing quaternion
		
		self.pi = 3.1415926535
		self.GyroMeasError = float(self.pi * ( 40 / 180 ))
		self.beta = float(math.sqrt(3 / 4) * self.GyroMeasError)

		self.GyroMeasDrift = float(self.pi * ( 2 / 180 ))
		self.zeta = float(math.sqrt(3 / 4) * self.GyroMeasDrift)


		self.beta = math.sqrt(3 / 4) * self.GyroMeasError

		self.q = [1,0,0,0]
#######################################################################################################################
#Speed subscriber
		self.motor_speed = rospy.Subscriber('/car/cmd_vel',Twist,self._Update_Speed)

#######################################################################################################################
	def _Update_Speed(self, speed):

		self._motor = speed.linear.x
		self._servo = speed.angular.z

		speed_message = 's %d %d\r' %(int(self._servo),int(self._motor))

		self._WriteSerial(speed_message)

#######################################################################################################################
#Calculate orientation from accelerometer and gyrometer

	def _HandleReceivedLine(self,  line):

		self._Counter = self._Counter + 1
		self._SerialPublisher.publish(String(str(self._Counter) + ", in:  " + line))

		if(len(line) > 0):

			lineParts = line.split('\t')
			try:

				if(lineParts[0] == 'b'):
					self._battery_value = float(lineParts[1])

#######################################################################################################################
					self._Battery_Level.publish(self._battery_value)

#######################################################################################################################
			
				if(lineParts[0] == 'i'):

					self._qx = float(lineParts[1])
					self._qy = float(lineParts[2])
					self._qz = float(lineParts[3])
					self._qw = float(lineParts[4])

#######################################################################################################################

					imu_msg = Imu()
					h = Header()
					h.stamp = rospy.Time.now()
					h.frame_id = self.frame_id

					imu_msg.header = h

					imu_msg.orientation_covariance = self.imu_data.orientation_covariance 	
					imu_msg.angular_velocity_covariance = self.imu_data.angular_velocity_covariance
					imu_msg.linear_acceleration_covariance = self.imu_data.linear_acceleration_covariance 

					imu_msg.orientation.x = self._qx
					imu_msg.orientation.y = self._qy
					imu_msg.orientation.z = self._qz
					imu_msg.orientation.w = self._qw
                                        #q_rot = quaternion_from_euler(self.pi, -self.pi/2, 0)
                                        #q_ori = Quaternion(self._qx, self._qy, self._qz, self._qw)
                                        #imu_msg.orientation = quaternion_multiply(q_ori, q_rot)
                                        self.imu_pub.publish(imu_msg)

			except:
				rospy.logwarn("Error in Sensor values")
				rospy.logwarn(lineParts)
				pass


#######################################################################################################################


	def _WriteSerial(self, message):
		self._SerialPublisher.publish(String(str(self._Counter) + ", out: " + message))
		self._SerialDataGateway.Write(message)

#######################################################################################################################


	def Start(self):
		rospy.logdebug("Starting")
	 	self._SerialDataGateway.Start()

#######################################################################################################################

	def Stop(self):
		rospy.logdebug("Stopping")
		self._SerialDataGateway.Stop()

#######################################################################################################################


	def Reset_TianBot_RACECAR(self):
		self._SerialDataGateway.Reset()
                time.sleep(3)


#######################################################################################################################

if __name__ =='__main__':
	rospy.init_node('TianBot_RACECAR_ros',anonymous=True)
	TianBot_RACECAR = TianBot_RACECAR_Class()
	try:
		
		TianBot_RACECAR.Start()
		rospy.spin()
	except rospy.ROSInterruptException:
		rospy.logwarn("Error in main function")


	TianBot_RACECAR.Reset_TianBot_RACECAR()
	TianBot_RACECAR.Stop()

#######################################################################################################################



# 硬件设备：

## 底盘：
$(find tianbot_racecar)/launch/RACECAR_core.launch

## IMU：
$(find tianbot_racecar)/launch/Device/gy85.launch

## 激光雷达：
$(find tianbot_racecar)/launch/Device/rplidar.launch


# RVIZ可视化：

## 激光雷达：
$(find tianbot_racecar)/launch/View/view_rplidar.launch

## IMU:
$(find tianbot_racecar)/launch/View/view_imu.launch

## 导航：
$(find tianbot_racecar)/launch/View/view_amcl.launch

## 建图：
$(find tianbot_racecar)/launch/View/view_gmapping.launch

## 查看由雷达生成的odom里程信息：
$(find tianbot_racecar)/launch/View/view_laser_odom.launch


# 功能包：

## 键盘控制：
+底盘
$(find tianbot_racecar)/launch/Teleop/keyboard_teleop.launch


## 手柄控制：
+底盘
$(find tianbot_racecar)/launch/Teleop/joystick_teleop.launch


## 导航：
+底盘
+IMU
+激光雷达
$(find tianbot_racecar)/launch/RACECAR_amcl_nav.launch

阳光明媚 备 2018.07.11日





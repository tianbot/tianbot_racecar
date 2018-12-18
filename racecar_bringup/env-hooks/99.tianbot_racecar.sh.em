# Set some defaults to tianbot racecar launch environment

: ${TIANBOT_RACECAR_BASE:=compact}  #compact, standard, full.
: ${TIANBOT_RACECAR_RGBD_CAMERA:=realsense_d435} #realsense_d415, realsense_d435, astra, astra_pro, xtion 
: ${TIANBOT_RACECAR_LIDAR:=rplidar_a3} # rplidar_a1, rplidar_a2, rplidar_a3
: ${TIANBOT_RACECAR_STEERING_REVERSE:=normal} # normal, reverse
: ${TIANBOT_RACECAR_THROTTLE_REVERSE:=normal} # normal, reverse


#Exports
export TIANBOT_RACECAR_BASE
export TIANBOT_RACECAR_RGBD_CAMERA
export TIANBOT_RACECAR_LIDAR
export TIANBOT_RACECAR_STEERING_REVERSE
export TIANBOT_RACECAR_THROTTLE_REVERSE

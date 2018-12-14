#!/bin/bash

echo "Install systemd service and enable racecar self boot"

sudo cp ./_service_/tianbot_racecar_bringup.service  /lib/systemd/system
sudo cp ./_bin_/tianbot_racecar_bringup.sh  /usr/local/bin
sudo chmod +x /usr/local/bin/tianbot_racecar_bringup.sh

echo " "
echo "Enable tianbot racecar self boot"
echo ""
sudo systemctl daemon-reload
sudo systemctl enable tianbot_racecar_bringup.service

echo "finish. "
echo "Use 'systemctl disable tianbot_racecar_bringup.service' to disable self boot "


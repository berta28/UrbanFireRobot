#!/bin/bash

# Update and install necessary packages
sudo apt update && sudo apt install -y curl gnupg2 lsb-release

# Add the ROS 2 GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# Add the ROS 2 repository
sudo sh -c 'echo "deb http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'

# Update and install ROS 2 Jammy
sudo apt update && sudo apt install -y ros-humble-desktop

# Source the ROS 2 setup script
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Create a workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
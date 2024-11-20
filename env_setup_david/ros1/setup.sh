#!/bin/bash

# Update and install necessary packages
sudo apt update

sudo apt install nano -y
sudo apt install python3-pip -y

#https://docs.clearpathrobotics.com/docs/ros1noetic/robots/outdoor_robots/jackal/tutorials_jackal/
sudo apt-get install -y ros-noetic-jackal-simulator ros-noetic-jackal-desktop ros-noetic-jackal-navigation

# # Source the ROS 2 setup script
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Create a workspace
# mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

rosdep install --from-paths src --ignore-src --rosdistro noetic -y

# colcon build
# chmod +x UrbanFireRobot/ros2_ws/src/warehouse_simulation/scripts/warehouse_generator.py
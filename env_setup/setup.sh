#!/bin/bash

# Update and install necessary packages
sudo apt update && sudo apt install -y curl gnupg2 lsb-release

# Add the ROS 1 GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# Add the ROS 1 repository
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros-latest.list'

# Update and install ROS 1 Noetic
sudo apt update && sudo apt install -y ros-noetic-desktop-full
sudo apt install -y python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential python3-rosdep pytohn3-pip python3-vcstool python3-colcon-common-extensions

#https://docs.clearpathrobotics.com/docs/ros1noetic/robots/outdoor_robots/jackal/tutorials_jackal/
sudo apt-get install -y ros-noetic-jackal-simulator ros-noetic-jackal-desktop ros-noetic-jackal-navigation
# Source the ROS 1 setup script
sudo apt-get update
sudo apt-get install lsb-release wget gnupg -y

sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt-get update -y
sudo apt-get install -y ignition-edifice

sudo apt-get install -y ros-noetic-ros-ign-gazebo
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
echo "export IGNITION_VERSION=edifice" >> ~/.bashrc
echo "export IGN_GAZEBO_RESOURCE_PATH=$IGN_GAZEBO_RESOURCE_PATH:~/UrbanFireRobot/ros2_ws/install/share/warehouse_simulation/models" >> ~/.bashrc
source ~/.bashrc

# Create a workspace
mkdir -p ~/UrbanFireRobot/ros2_ws/src
cd ~/UrbanFireRobot/ros2_ws
colcon build
rosdep install --from-paths src --ignore-src --rosdistro noetic -y

source ~/UrbanFireRobot/ros2_ws/install/setup.bash

chmod +x UrbanFireRobot/ros2_ws/src/warehouse_simulation/scripts/warehouse_generator.py

# export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/UrbanFireRobot/ros2_ws/install/share/warehouse_simulation/models
export IGN_GAZEBO_RESOURCE_PATH=$IGN_GAZEBO_RESOURCE_PATH:~/UrbanFireRobot/ros2_ws/install/share/warehouse_simulation/models
# export IGN_CONFIG_PATH=/usr/share/ignition
# export IGN_GAZEBO_SYSTEM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/ign-gazebo-3/system_plugins
# export IGN_GAZEBO_RESOURCE_PATH=$IGN_GAZEBO_RESOURCE_PATH:$HOME/.ignition/fuel/fuel.ignitionrobotics.org/openrobotics/models



# export LIBGL_ALWAYS_SOFTWARE=true


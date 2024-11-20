# Use the official ROS 1 noetic base image
FROM osrf/ros:noetic-desktop-full

# Set the working directory
WORKDIR /root

# Copy the setup script into the container
COPY setup.sh /root/setup.sh

# Make the setup script executable
RUN chmod +x /root/setup.sh

# Source the ROS 2 setup script
RUN bash /root/setup.sh
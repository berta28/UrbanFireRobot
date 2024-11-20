cmake_minimum_required(VERSION 3.0.2)
project(warehouse_simulation)

find_package(catkin REQUIRED COMPONENTS
  rospy
  ros_ign_gazebo
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/warehouse_generator.py
  scripts/object_detector.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY models/
  DESTINATION share/${PROJECT_NAME}/models
)

install(
  DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

install(
  DIRECTORY worlds/
  DESTINATION share/${PROJECT_NAME}/worlds
)
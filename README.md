# UrbanFireRobot
RBECapstone

## Overview

This repository contains the code and resources for the UrbanFireRobot project, developed as part of the RBECapstone. The project utilizes ROS 2 Jammy for robotic control and simulation.

## Setup Instructions

More information of jackal intergration see https://docs.clearpathrobotics.com/docs/ros1noetic/robots/outdoor_robots/jackal/tutorials_jackal/

### Using Docker

To set up the ROS 2 Jammy environment using Docker, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/UrbanFireRobot.git
    cd UrbanFireRobot
    ```

2. **Build and run the Docker container**:
    ```sh
    docker-compose up --build
    ```

This will build the Docker image and start a container with the ROS 2 Jammy environment. The `ros2_ws` folder in the repository will be mounted into the container at `/root/ros2_ws`.

### Native Linux Setup

To set up the ROS 2 Jammy environment natively on a Linux machine, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/UrbanFireRobot.git
    cd UrbanFireRobot
    ```

2. **Run the setup script**:
    ```sh
    chmod +x setup.sh
    ./setup.sh
    ```

This script will install ROS 2 Jammy and set up the workspace in `~/ros2_ws`.

## Workspace Structure

- `ros2_ws`: The ROS 2 workspace where all packages and code for the project are located.

## Running the simulation

After building (catkin_make) you also need to source the workspace setup.bash:
`source devel/setup.bash`

To indicate the path to the built models also do:
`export GAZEBO_MODEL_PATH=~/ros2_ws/src/warehouse_simulation/models`

To add the camera sensors to the model also do the following:
`export JACKAL_URDF_EXTRAS=~/ros2_ws/src/warehouse_simulation/description/camera.xacro`

To start gazebo and the simulation run the command `roslaunch warehouse_simulation warehouse_simulation.launch world_file:=warehouse_full.world` 

// Adding people to the world can be done by `ros2 launch warehouse_simulation warehouse_generator.py`

## Contributing

Please follow the standard GitHub flow for contributing:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
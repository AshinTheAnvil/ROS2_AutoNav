cmake_minimum_required(VERSION 3.5)
project(myrobot_description)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(xacro REQUIRED)
#find_package(robot_state_publisher REQUIRED)
##find_package(geometry_msgs REQUIRED)
#find_package(sensor_msgs REQUIRED)
#find_package(tf2 REQUIRED)
#find_package(tf2_ros REQUIRED)
#find_package(gazebo_ros REQUIRED)

# Install URDF and launch files
install(DIRECTORY urdf launch meshes worlds
  DESTINATION share/${PROJECT_NAME}
)

# This is required for ROS 2 packages
ament_package()


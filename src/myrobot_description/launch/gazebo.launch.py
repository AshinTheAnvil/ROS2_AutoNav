import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import launch_ros.descriptions
from launch_ros.parameter_descriptions import ParameterValue
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Get package directory
    pkg_share = get_package_share_directory('myrobot_description')

    # XACRO file path
    xacro_file = os.path.join(pkg_share, 'urdf', 'my_robot.xacro')

    # Process XACRO to URDF
    robot_description_config = xacro.process_file(xacro_file).toxml()

    # RViz config file (optional)
    rviz_config_file = os.path.join(pkg_share, 'launch', 'display.rviz')
    if not os.path.exists(rviz_config_file):
        rviz_config_file = ''  # RViz will open default

    # Optional: Gazebo world file
    world_file = os.path.join(pkg_share, 'worlds', 'empty.world')

    return LaunchDescription([
        # Launch Gazebo Harmonic
        ExecuteProcess(
            cmd=['gz', 'sim', world_file, '-v', '4'],
            output='screen'
        ),

        # Spawn robot into Gazebo
        # Spawn robot
        # ExecuteProcess(
        #     cmd=['gz', 'create', '-topic', 'robot_description', '-entity', 'my_robot'],
        #     output='screen'
        # ),
        
        Node(
            package="ros_gz_sim",
            executable="create",
            arguments=[
            "-name",
            "robot1",
            "-topic",
            "robot_description",
            "-x",
            "0",
            "-y",
            "0",
            "-z",
            "0",
            ],
            output="screen",
        ),

        # Joint State Publisher (without GUI)
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'use_gui': False}],
            output='screen'
        ),


        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_config}]
        ),


        # Node(
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     name='chassis_to_camera_tf',
        #     arguments=['0.2', '0', '0', '0', '0', '0', 'chassis', 'camera']
        # ),

        # Node(
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     name='chassis_to_hokuyo_tf',
        #     arguments=['0.15', '0', '0.1', '0', '0', '0', 'chassis', 'hokuyo']
        # ),


        # RViz2
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_file] if rviz_config_file else []
        )
    ])

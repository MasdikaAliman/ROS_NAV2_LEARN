from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import Node

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    package_name = "bumperbot_description"

    # Load the robot model
    model_path = os.path.join(get_package_share_directory(package_name), "urdf", "bumperbot.urdf.xacro")
    # robot_description = ParameterValue(Command(["xacro ", model_path]), value_type=str)
    robot_description_content = xacro.process_file(model_path).toxml()
    robot_description = robot_description_content
    # Declare launch arguments
    model_arg = DeclareLaunchArgument(name="model", default_value=model_path, description="Model Path URDF FILE")

    # Robot State Publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}, {"use_sim_time": True}]
    )

    # Joint State Publisher GUI
    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        parameters=[{"use_sim_time": True}]
    )

    # RViz
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(get_package_share_directory(package_name), "rviz", "display_rviz.rviz")]
    )

    # Gazebo
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'))
    )

    # Spawn Robot in Gazebo
    spawn_entity = Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description',
                      '-entity', 'your_robot_name'],
            output='screen'
        )


    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller" ,"--controller-manager", "/controller_manager"],
    )


    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )


    return LaunchDescription([
        model_arg,
        robot_state_publisher,
        # joint_state_publisher_gui,
        rviz_node,
        # gazebo_launch,
    
        # diff_drive_spawner,
        # joint_state_broadcaster_spawner,
            # spawn_entity
    ])

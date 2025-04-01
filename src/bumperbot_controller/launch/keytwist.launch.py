from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    key_twist_node = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        parameters=[{'use_sim_time' : use_sim_time}],
        prefix="gnome-terminal --",  # Opens a terminal for input
        output='screen',
        remappings=[('/cmd_vel','/diff_control/keyboard/cmd_vel')]
       
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'), 
        key_twist_node   
    ])
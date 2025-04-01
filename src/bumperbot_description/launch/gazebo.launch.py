import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro
def generate_launch_description():
    package_name = "bumperbot_description"

    # Define world file path correctly
    world_model = os.path.join(get_package_share_directory(package_name), "worlds", "small_house.world")

    # Declare world launch argument
    world_arg = DeclareLaunchArgument(
        name="world",
        default_value=world_model,
        description="Gazebo world file"
    )


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


    # Gazebo server with world argument
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': LaunchConfiguration("world"), 'use_sim_time': 'True'}.items()  # Ensure argument is passed correctly
    )


    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"
                   ]
    )
    
    wheel_controller_spawner = Node(
            package= "controller_manager",
            executable="spawner",
            arguments=["bumperbot_controller"
                       ]
    )
    


    # Gazebo client
    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gzclient.launch.py')
        )
    )

    # Spawn robot entity in Gazebo
    spawn_entity = Node(
    package='gazebo_ros',
    executable='spawn_entity.py',
    arguments=['-topic', 'robot_description', '-entity', 'my_bot', '-x', '0', '-y', '0', '-z', '0.1', '-R', '0', '-P', '0', '-Y', '0'],
    output='screen'
    )

    return LaunchDescription([
        world_arg,
        DeclareLaunchArgument(name='gui', default_value='true'),
        DeclareLaunchArgument(name='use_sim_time', default_value='true'),
        robot_state_publisher,
        gazebo_server,
        # wheel_controller_spawner,
        # joint_state_broadcaster_spawner,
        gazebo_client,
        spawn_entity
    ])

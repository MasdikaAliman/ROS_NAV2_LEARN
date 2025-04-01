from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition, IfCondition
def generate_launch_description():
    
    wheel_radius_arg = DeclareLaunchArgument("wheel_radius", default_value="0.033")
    wheel_separation_arg = DeclareLaunchArgument("wheel_separation", default_value="0.17")
    use_sim_time_arg = DeclareLaunchArgument("use_sim_time", default_value= "True")
    use_my_controller_arg = DeclareLaunchArgument("use_my_controller", default_value="False")
    
    
    use_sim_time = LaunchConfiguration("use_sim_time")
    wheel_radius = LaunchConfiguration("wheel_radius")
    wheel_separation = LaunchConfiguration("wheel_separation")
    use_my_controller = LaunchConfiguration("use_my_controller")
    
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
                       ],
            condition=UnlessCondition(use_my_controller)
    )
    
    
    simple_velocity_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["simple_velocity_controller"
                   ],
        condition=IfCondition(use_my_controller)
    )
    
    my_controller_spawner = Node(
        package="bumperbot_controller",
        executable="bumperbot_controller",
        parameters=[{
            "wheel_radius": wheel_radius,
            "wheel_separation": wheel_separation,
            "use_sim_time": use_sim_time
        }],
        condition=IfCondition(use_my_controller)
    )
    return LaunchDescription([
        wheel_radius_arg,
        wheel_separation_arg,
        use_sim_time_arg,
        use_my_controller_arg,
        joint_state_broadcaster_spawner,
        wheel_controller_spawner,
        simple_velocity_spawner,
        my_controller_spawner
    ])
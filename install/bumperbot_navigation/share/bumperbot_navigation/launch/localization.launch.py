import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml
from icecream import ic

def generate_launch_description():
    our_package = "bumperbot_navigation"
    param_path = os.path.join(get_package_share_directory(our_package), "config", "nav2_param.yaml")
    map_path = os.path.join(get_package_share_directory(our_package),'map', 'map.yaml')
    slam_param_path = os.path.join(get_package_share_directory(our_package), "config", "slam_toolbox.yaml")
    
    ic(map_path, param_path)
    use_sim_time_arg = DeclareLaunchArgument("use_sim_time", default_value= "True")
    autostart_arg = DeclareLaunchArgument("autostart", default_value="True")
    params_file_arg = DeclareLaunchArgument('params_file', default_value=param_path)
    map_file_arg = DeclareLaunchArgument('map', default_value=map_path)

    map_yaml_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')
    
    lifecylce_nodes = ['map_server', "amcl"]
    
    
    param_substitutions = {
        'use_sim_time': use_sim_time,
        'yaml_filename': map_yaml_file}
    
    
    configured_params = RewrittenYaml(
        source_file=params_file,
        # root_key=namespace,
        param_rewrites=param_substitutions,
        convert_types=True)
    
    ic(configured_params, "cok")
    map_server_node = Node(
        package="nav2_map_server",
        executable="map_server",
        output="screen",
        parameters=[{"yaml_filename": map_yaml_file}, {"use_sim_time": use_sim_time}]
    )
    
    nav2_lifecyle_node = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}, {"autostart": autostart}, {"node_names": lifecylce_nodes}]
    )    

    nav2_amcl = Node(
        package="nav2_amcl",
        executable="amcl",
        output ="screen",
        parameters=[configured_params]
    )

    start_async_slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[slam_param_path],
        output='screen')

    return LaunchDescription([
        use_sim_time_arg, 
        autostart_arg, 
        params_file_arg, 
        map_file_arg,
        map_server_node,
        nav2_lifecyle_node,
        nav2_amcl,
        # start_async_slam_toolbox_node
        ])
    


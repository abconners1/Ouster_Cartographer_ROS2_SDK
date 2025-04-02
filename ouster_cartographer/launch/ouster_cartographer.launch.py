import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    cartographer_config_dir = LaunchConfiguration('cartographer_config_dir')
    configuration_basename = LaunchConfiguration('configuration_basename')
    
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')
        
    pkg_dir = get_package_share_directory('ouster_cartographer')
    
    declare_cartographer_config_dir = DeclareLaunchArgument(
        'cartographer_config_dir',
        default_value=os.path.join(pkg_dir, 'config'),
        description='Full path to config file directory')
        
    declare_configuration_basename = DeclareLaunchArgument(
        'configuration_basename',
        default_value='ouster_lidar.lua',
        description='Name of lua file for cartographer')
    
    # Static TF nodes
    base_to_sensor = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_to_sensor',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'os_sensor']
    )
    
    sensor_to_lidar = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='sensor_to_lidar',
        arguments=['0', '0', '0', '0', '0', '0', 'os_sensor', 'os_lidar']
    )
    
    # Cartographer node
    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-configuration_directory', cartographer_config_dir,
                   '-configuration_basename', configuration_basename],
        remappings=[('scan', '/ouster/scan')]
    )
    
    # Occupancy grid node
    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='occupancy_grid_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-resolution', '0.05']
    )
    
    # RVIZ node
    rviz_config_file = os.path.join(pkg_dir, 'config', 'ouster_cartographer.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )
    
    return LaunchDescription([
        declare_use_sim_time,
        declare_cartographer_config_dir,
        declare_configuration_basename,
        base_to_sensor,
        sensor_to_lidar,
        cartographer_node,
        occupancy_grid_node,
        rviz_node
    ])

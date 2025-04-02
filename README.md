# Ouster_Cartographer_ROS2_SDK
Implementing the Ouster SDK published Lidar data into Google Cartographer for point cloud SLAM
Ouster Cartographer SLAM

This repository demonstrates using Cartographer with an Ouster LiDAR sensor on ROS 2 (tested on Jazzy + Ubuntu 24.04). It includes:

    A launch file to replay a PCAP file from the Ouster SDK.

    A Cartographer configuration (both 2D and 3D options) tailored for Ouster LiDAR data.

    Example instructions on how to visualize and build SLAM maps in RViz.

A brief demo video is available here:
https://youtu.be/brJVr-w-MLs

Features

    2D Cartographer with Ouster LiDAR scans.

    3D Cartographer support if you prefer generating full 3D point clouds.

    Configuration examples for using IMU data from your Ouster sensor (recommended for moving vehicles).

    Launch files for easy replay of .pcap recordings as well as real-time scanning.

Requirements

    ROS 2 Jazzy (or later)

    Ubuntu 24.04 (or a compatible ROS 2 platform)

    Ouster ROS 2 SDK for reading .pcap files

    Cartographer ROS

Installation

    Clone this repository into your ROS 2 workspace:

cd ~/ros2_ws/src
git clone https://github.com/your_username/ouster_cartographer.git

Install dependencies (example):

cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -y

Build:

colcon build

Source your workspace:

    source ~/ros2_ws/install/setup.bash

Usage
1. Replay Ouster PCAP

    Place your .pcap and .json files in a known directory, e.g. ~/Downloads/.

    Launch the Ouster replay node:

    ros2 launch ouster_ros replay_pcap.launch.xml \
      pcap_file:=/home/myuser/Downloads/sample.pcap \
      metadata:=/home/myuser/Downloads/sample.json \
      use_sim_time:=true \
      viz:=false

    This publishes the Ouster data (scan or pointcloud) on ROS topics like /ouster/scan and /ouster/points.

2. Run Cartographer

In another terminal (also sourced), launch the Cartographer SLAM:

ros2 launch ouster_cartographer ouster_cartographer.launch.py

By default, this runs a 2D Cartographer setup, listening to /ouster/scan. It will start RViz automatically (unless configured otherwise) and show the occupancy grid map.

    Tip: If you want to switch to the 3D pipeline, modify ouster_lidar.lua:

    MAP_BUILDER.use_trajectory_builder_3d = true
    num_point_clouds = 1
    num_laser_scans = 0
    ...

    and update the launch file to remap point_cloud → /ouster/points.

Common Tips & Troubleshooting

    Noisy Maps?

        Enable IMU data:

TRAJECTORY_BUILDER_2D.use_imu_data = true
tracking_frame = "os_imu"

Provide odometry if available:

        use_odometry = true
        odom_frame = "odom"

    Frame Transform Issues
    Ensure you have correct TF trees:
    base_link -> os_sensor -> os_lidar -> os_imu
    or whichever chain matches your physical setup.

    RViz Message Filter Warnings
    Raise the “Queue Size” in RViz displays if you see queue is full.

Demo Video

Watch a quick demonstration of Ouster LiDAR with Cartographer in action:
Ouster Cartographer Demo on YouTube
Contributing

Feel free to open issues or pull requests if you have improvements or suggestions. Please make sure to follow the ROS 2 community guidelines.
License

This repository is licensed under the MIT License (or choose your license).
See LICENSE for details.

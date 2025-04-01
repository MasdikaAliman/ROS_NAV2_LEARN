# How To Build
- Install package
```
  rosdep install --from-paths my_package --ignore-src -r -y
```
- Build
```
  colcon build
```

# How To Run
Source Package first: 
```
source install/setup.bash
```

- Run the Gazebo
```
ros2 launch bumperbot_description gazebo.launch.py
```

- Run the rviz
```
ros2 launch bumperbot_description rviz_display.launch.py
```
- Run the Localization
```
ros2 launch bumperbot_navigation localization.launch.py
```
- Run the navigation
```
ros2 launch bumperbot_navigation navigation.launch.py
```

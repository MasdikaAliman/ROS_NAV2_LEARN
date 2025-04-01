cmake_minimum_required(VERSION 3.8)
project(bumperbot_controller)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(Eigen3 REQUIRED)


include_directories(include)
include_directories(${EIGEN3_INCLUDE_DIR})

add_executable(bumperbot_controller src/diff_kinematic.cpp)
ament_target_dependencies(bumperbot_controller rclcpp geometry_msgs std_msgs ${Eigen_LIBRARIES})

install(
  DIRECTORY include
  DESTINATION include
)

install(TARGETS
bumperbot_controller
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)


ament_package()

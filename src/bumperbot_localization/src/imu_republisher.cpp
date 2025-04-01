#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"

using namespace std::chrono_literals;

rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr imu_pub;

void IMU_CB(const sensor_msgs::msg::Imu &imu){
    sensor_msgs::msg::Imu new_data;

    new_data = imu;
    new_data.header.frame_id = "base_footprint_ekf";
    imu_pub->publish(new_data);
}


int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node> ("imu_node_republisher");
    rclcpp::sleep_for(1s);
    imu_pub = node->create_publisher<sensor_msgs::msg::Imu>("imu_ekf", 10);
    auto imu_sub = node->create_subscription<sensor_msgs::msg::Imu>("/imu_plugin/out", 10 , IMU_CB);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

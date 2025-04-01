#include "odom_republisher.hpp"
using std::placeholders::_1;
OdomRepublish::OdomRepublish(const std::string &name) : Node(name)
{

    this->odom_pub = this->create_publisher<nav_msgs::msg::Odometry>("/bumperbot_controller/odom_noisy", 10);
    this->odom_sub = this->create_subscription<nav_msgs::msg::Odometry>("/bumperbot_controller/odom", 10, std::bind(&OdomRepublish::odomCB, this, _1));
}

void OdomRepublish::odomCB(const nav_msgs::msg::Odometry &data)
{
    nav_msgs::msg::Odometry new_data;

    new_data = data;
    new_data.header.frame_id = "odom";
    new_data.child_frame_id = "base_footprint_ekf";

    odom_pub->publish(new_data);
}

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<OdomRepublish> ("odom_repub_node");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

#ifndef ODOM_REPUBLISH
#define ODOM_REPUBLISH
#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/msg/odometry.hpp"

class OdomRepublish : public rclcpp::Node
{
public:
    OdomRepublish(const std::string &name);

private:
    void odomCB(const nav_msgs::msg::Odometry &data);

    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odom_sub;
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_pub;
};



#endif
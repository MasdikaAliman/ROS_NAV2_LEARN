#ifndef DIF_KINEMATIC_HPP
#define DIF_KINEMATIC_HPP
#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist_stamped.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <std_msgs/msg/float64_multi_array.hpp>
#include "eigen3/Eigen/Core"

namespace rclcpp
{

    class DiffController : public Node
    {
    public:
        DiffController(const std::string &name);

    private:
        void velocity_joy_cb(const geometry_msgs::msg::TwistStamped msg);
        void velocity_key_cb(const geometry_msgs::msg::Twist msg);
        Subscription<geometry_msgs::msg::TwistStamped>::SharedPtr vel_joy_sub;
        Subscription<geometry_msgs::msg::Twist>::SharedPtr vel_key_sub;
        Publisher<std_msgs::msg::Float64MultiArray> ::SharedPtr wheel_cmd_pub_;
        Eigen::Matrix2d speed_conversion_;
        double wheel_radius_, wheel_separation_;
    };

};
#endif
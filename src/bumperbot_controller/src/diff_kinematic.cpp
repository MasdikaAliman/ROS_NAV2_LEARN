#include "dif_kinematic.hpp"
#include "eigen3/Eigen/Geometry"
using std::placeholders::_1; // this for single callback only if i have multiple arg use _2 for 2 arg in callback
namespace rclcpp
{
    DiffController::DiffController(const std::string &name) : Node(name)
    {
        this->declare_parameter("wheel_radius", 0.033);
        this->declare_parameter("wheel_separation", 0.17);

        wheel_radius_ = this->get_parameter("wheel_radius").as_double();
        wheel_separation_ = this->get_parameter("wheel_separation").as_double();

        RCLCPP_INFO_STREAM(this->get_logger(), "Wheel Radius: " << wheel_radius_);
        RCLCPP_INFO_STREAM(this->get_logger(), "Wheel Separation: " << wheel_separation_);

        speed_conversion_ << wheel_radius_ / 2, wheel_radius_ / 2,
            wheel_radius_ / wheel_separation_, -wheel_radius_ / wheel_separation_;

        // Init subs and Publisher
        vel_joy_sub = create_subscription<geometry_msgs::msg::TwistStamped>("/diff_control/joy/cmd_vel", 10, std::bind(&DiffController::velocity_joy_cb, this, _1));
        wheel_cmd_pub_ = create_publisher<std_msgs::msg::Float64MultiArray>("/simple_velocity_controller/commands", 10); // Publish to topic velocity_controllers ros2 control
        vel_key_sub = create_subscription<geometry_msgs::msg::Twist>("/diff_control/keyboard/cmd_vel", 10, std::bind(&DiffController::velocity_key_cb, this, _1));
        RCLCPP_INFO_STREAM(this->get_logger(), "Speed Conversion Matrix: " << speed_conversion_);
    }

    void DiffController::velocity_joy_cb(const geometry_msgs::msg::TwistStamped msg)
    {
        Eigen::Vector2d robot_speed(msg.twist.linear.x, msg.twist.angular.z);
        Eigen::Vector2d wheel_speed = speed_conversion_.inverse() * robot_speed;

        std_msgs::msg::Float64MultiArray wheel_speed_msg_;
        wheel_speed_msg_.data.push_back(wheel_speed.coeff(1));
        wheel_speed_msg_.data.push_back(wheel_speed.coeff(0));

        wheel_cmd_pub_->publish(wheel_speed_msg_);
    }

    void DiffController::velocity_key_cb(const geometry_msgs::msg::Twist msg)
    {
        Eigen::Vector2d robot_speed(msg.linear.x ,msg.angular.z);
        Eigen::Vector2d wheel_speed = speed_conversion_.inverse() * robot_speed;

        std_msgs::msg::Float64MultiArray wheel_speed_msg_;
        wheel_speed_msg_.data.push_back(wheel_speed.coeff(1));
        wheel_speed_msg_.data.push_back(wheel_speed.coeff(0));

        wheel_cmd_pub_->publish(wheel_speed_msg_);
    }

};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto diff_node = std::make_shared<rclcpp::DiffController>("diff_node");
    rclcpp::spin(diff_node);
    rclcpp::shutdown();
    return 0;
}

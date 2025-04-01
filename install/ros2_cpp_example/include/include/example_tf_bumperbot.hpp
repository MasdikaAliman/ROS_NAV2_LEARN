#ifndef SIMPLE_TF2
#define SIMPLE_TF2

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_ros/static_transform_broadcaster.h"

class SimpleTF2 : public rclcpp::Node
{

public:
    SimpleTF2(const std::string &name);

private:
    void timerCallback();

    geometry_msgs::msg::TransformStamped static_transform_stamped;
    std::shared_ptr<tf2_ros::StaticTransformBroadcaster> static_tf_broadcaster;


    double last_x_;
    double x_inc_;
    double rotation_counter_;

};



#endif
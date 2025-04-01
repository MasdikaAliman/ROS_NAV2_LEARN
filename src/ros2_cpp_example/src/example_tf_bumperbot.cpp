#include "icecream.hpp"
#include "example_tf_bumperbot.hpp"

SimpleTF2::SimpleTF2(const std::string &name) : Node(name),
                                                last_x_(0.0), x_inc_(0.05), rotation_counter_(0)
{
    static_tf_broadcaster = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

    // Static Transform
    static_transform_stamped.header.stamp = get_clock()->now();
    static_transform_stamped.header.frame_id = "world";
    static_transform_stamped.child_frame_id = "bumperbot_base";
    static_transform_stamped.transform.translation.x = 0.5;
    static_transform_stamped.transform.translation.y = 0;
    static_transform_stamped.transform.translation.z = 0;

    static_transform_stamped.transform.rotation.w = 1.0;
    static_transform_stamped.transform.rotation.x = 0;
    static_transform_stamped.transform.rotation.y = 0;
    static_transform_stamped.transform.rotation.z = 0;

    static_tf_broadcaster->sendTransform(static_transform_stamped);

    RCLCPP_INFO_STREAM(get_logger(), "Publishing static transform between " << static_transform_stamped.header.frame_id << " and " << static_transform_stamped.child_frame_id);
}

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<SimpleTF2>("simple_tf2");

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

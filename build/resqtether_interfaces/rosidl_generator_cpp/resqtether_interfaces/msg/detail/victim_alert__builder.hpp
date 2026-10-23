// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from resqtether_interfaces:msg/VictimAlert.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "resqtether_interfaces/msg/victim_alert.hpp"


#ifndef RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__BUILDER_HPP_
#define RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "resqtether_interfaces/msg/detail/victim_alert__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace resqtether_interfaces
{

namespace msg
{

namespace builder
{

class Init_VictimAlert_notes
{
public:
  explicit Init_VictimAlert_notes(::resqtether_interfaces::msg::VictimAlert & msg)
  : msg_(msg)
  {}
  ::resqtether_interfaces::msg::VictimAlert notes(::resqtether_interfaces::msg::VictimAlert::_notes_type arg)
  {
    msg_.notes = std::move(arg);
    return std::move(msg_);
  }

private:
  ::resqtether_interfaces::msg::VictimAlert msg_;
};

class Init_VictimAlert_delay_seconds
{
public:
  explicit Init_VictimAlert_delay_seconds(::resqtether_interfaces::msg::VictimAlert & msg)
  : msg_(msg)
  {}
  Init_VictimAlert_notes delay_seconds(::resqtether_interfaces::msg::VictimAlert::_delay_seconds_type arg)
  {
    msg_.delay_seconds = std::move(arg);
    return Init_VictimAlert_notes(msg_);
  }

private:
  ::resqtether_interfaces::msg::VictimAlert msg_;
};

class Init_VictimAlert_deferred_relay
{
public:
  explicit Init_VictimAlert_deferred_relay(::resqtether_interfaces::msg::VictimAlert & msg)
  : msg_(msg)
  {}
  Init_VictimAlert_delay_seconds deferred_relay(::resqtether_interfaces::msg::VictimAlert::_deferred_relay_type arg)
  {
    msg_.deferred_relay = std::move(arg);
    return Init_VictimAlert_delay_seconds(msg_);
  }

private:
  ::resqtether_interfaces::msg::VictimAlert msg_;
};

class Init_VictimAlert_rssi_at_transmission
{
public:
  explicit Init_VictimAlert_rssi_at_transmission(::resqtether_interfaces::msg::VictimAlert & msg)
  : msg_(msg)
  {}
  Init_VictimAlert_deferred_relay rssi_at_transmission(::resqtether_interfaces::msg::VictimAlert::_rssi_at_transmission_type arg)
  {
    msg_.rssi_at_transmission = std::move(arg);
    return Init_VictimAlert_deferred_relay(msg_);
  }

private:
  ::resqtether_interfaces::msg::VictimAlert msg_;
};

class Init_VictimAlert_rssi_at_detection
{
public:
  explicit Init_VictimAlert_rssi_at_detection(::resqtether_interfaces::msg::VictimAlert & msg)
  : msg_(msg)
  {}
  Init_VictimAlert_rssi_at_transmission rssi_at_detection(::resqtether_interfaces::msg::VictimAlert::_rssi_at_detection_type arg)
  {
    msg_.rssi_at_detection = std::move(arg);
    return Init_VictimAlert_rssi_at_transmission(msg_);
  }

private:
  ::resqtether_interfaces::msg::VictimAlert msg_;
};

class Init_VictimAlert_victim_y
{
public:
  explicit Init_VictimAlert_victim_y(::resqtether_interfaces::msg::VictimAlert & msg)
  : msg_(msg)
  {}
  Init_VictimAlert_rssi_at_detection victim_y(::resqtether_interfaces::msg::VictimAlert::_victim_y_type arg)
  {
    msg_.victim_y = std::move(arg);
    return Init_VictimAlert_rssi_at_detection(msg_);
  }

private:
  ::resqtether_interfaces::msg::VictimAlert msg_;
};

class Init_VictimAlert_victim_x
{
public:
  explicit Init_VictimAlert_victim_x(::resqtether_interfaces::msg::VictimAlert & msg)
  : msg_(msg)
  {}
  Init_VictimAlert_victim_y victim_x(::resqtether_interfaces::msg::VictimAlert::_victim_x_type arg)
  {
    msg_.victim_x = std::move(arg);
    return Init_VictimAlert_victim_y(msg_);
  }

private:
  ::resqtether_interfaces::msg::VictimAlert msg_;
};

class Init_VictimAlert_stamp
{
public:
  Init_VictimAlert_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VictimAlert_victim_x stamp(::resqtether_interfaces::msg::VictimAlert::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_VictimAlert_victim_x(msg_);
  }

private:
  ::resqtether_interfaces::msg::VictimAlert msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::resqtether_interfaces::msg::VictimAlert>()
{
  return resqtether_interfaces::msg::builder::Init_VictimAlert_stamp();
}

}  // namespace resqtether_interfaces

#endif  // RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__BUILDER_HPP_

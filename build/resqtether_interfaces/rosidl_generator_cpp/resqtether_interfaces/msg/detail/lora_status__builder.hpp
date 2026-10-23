// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from resqtether_interfaces:msg/LoraStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "resqtether_interfaces/msg/lora_status.hpp"


#ifndef RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__BUILDER_HPP_
#define RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "resqtether_interfaces/msg/detail/lora_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace resqtether_interfaces
{

namespace msg
{

namespace builder
{

class Init_LoraStatus_snr
{
public:
  explicit Init_LoraStatus_snr(::resqtether_interfaces::msg::LoraStatus & msg)
  : msg_(msg)
  {}
  ::resqtether_interfaces::msg::LoraStatus snr(::resqtether_interfaces::msg::LoraStatus::_snr_type arg)
  {
    msg_.snr = std::move(arg);
    return std::move(msg_);
  }

private:
  ::resqtether_interfaces::msg::LoraStatus msg_;
};

class Init_LoraStatus_rssi
{
public:
  explicit Init_LoraStatus_rssi(::resqtether_interfaces::msg::LoraStatus & msg)
  : msg_(msg)
  {}
  Init_LoraStatus_snr rssi(::resqtether_interfaces::msg::LoraStatus::_rssi_type arg)
  {
    msg_.rssi = std::move(arg);
    return Init_LoraStatus_snr(msg_);
  }

private:
  ::resqtether_interfaces::msg::LoraStatus msg_;
};

class Init_LoraStatus_sender_id
{
public:
  explicit Init_LoraStatus_sender_id(::resqtether_interfaces::msg::LoraStatus & msg)
  : msg_(msg)
  {}
  Init_LoraStatus_rssi sender_id(::resqtether_interfaces::msg::LoraStatus::_sender_id_type arg)
  {
    msg_.sender_id = std::move(arg);
    return Init_LoraStatus_rssi(msg_);
  }

private:
  ::resqtether_interfaces::msg::LoraStatus msg_;
};

class Init_LoraStatus_stamp
{
public:
  Init_LoraStatus_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LoraStatus_sender_id stamp(::resqtether_interfaces::msg::LoraStatus::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_LoraStatus_sender_id(msg_);
  }

private:
  ::resqtether_interfaces::msg::LoraStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::resqtether_interfaces::msg::LoraStatus>()
{
  return resqtether_interfaces::msg::builder::Init_LoraStatus_stamp();
}

}  // namespace resqtether_interfaces

#endif  // RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__BUILDER_HPP_

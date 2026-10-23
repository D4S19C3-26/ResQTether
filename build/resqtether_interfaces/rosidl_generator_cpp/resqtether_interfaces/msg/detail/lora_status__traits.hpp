// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from resqtether_interfaces:msg/LoraStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "resqtether_interfaces/msg/lora_status.hpp"


#ifndef RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__TRAITS_HPP_
#define RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "resqtether_interfaces/msg/detail/lora_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace resqtether_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const LoraStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
    out << ", ";
  }

  // member: sender_id
  {
    out << "sender_id: ";
    rosidl_generator_traits::value_to_yaml(msg.sender_id, out);
    out << ", ";
  }

  // member: rssi
  {
    out << "rssi: ";
    rosidl_generator_traits::value_to_yaml(msg.rssi, out);
    out << ", ";
  }

  // member: snr
  {
    out << "snr: ";
    rosidl_generator_traits::value_to_yaml(msg.snr, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LoraStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }

  // member: sender_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sender_id: ";
    rosidl_generator_traits::value_to_yaml(msg.sender_id, out);
    out << "\n";
  }

  // member: rssi
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rssi: ";
    rosidl_generator_traits::value_to_yaml(msg.rssi, out);
    out << "\n";
  }

  // member: snr
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "snr: ";
    rosidl_generator_traits::value_to_yaml(msg.snr, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LoraStatus & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace resqtether_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use resqtether_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const resqtether_interfaces::msg::LoraStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  resqtether_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use resqtether_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const resqtether_interfaces::msg::LoraStatus & msg)
{
  return resqtether_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<resqtether_interfaces::msg::LoraStatus>()
{
  return "resqtether_interfaces::msg::LoraStatus";
}

template<>
inline const char * name<resqtether_interfaces::msg::LoraStatus>()
{
  return "resqtether_interfaces/msg/LoraStatus";
}

template<>
struct has_fixed_size<resqtether_interfaces::msg::LoraStatus>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<resqtether_interfaces::msg::LoraStatus>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<resqtether_interfaces::msg::LoraStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__TRAITS_HPP_

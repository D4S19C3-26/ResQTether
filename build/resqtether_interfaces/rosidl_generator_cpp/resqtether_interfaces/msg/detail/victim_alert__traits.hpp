// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from resqtether_interfaces:msg/VictimAlert.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "resqtether_interfaces/msg/victim_alert.hpp"


#ifndef RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__TRAITS_HPP_
#define RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "resqtether_interfaces/msg/detail/victim_alert__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace resqtether_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const VictimAlert & msg,
  std::ostream & out)
{
  out << "{";
  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
    out << ", ";
  }

  // member: victim_x
  {
    out << "victim_x: ";
    rosidl_generator_traits::value_to_yaml(msg.victim_x, out);
    out << ", ";
  }

  // member: victim_y
  {
    out << "victim_y: ";
    rosidl_generator_traits::value_to_yaml(msg.victim_y, out);
    out << ", ";
  }

  // member: rssi_at_detection
  {
    out << "rssi_at_detection: ";
    rosidl_generator_traits::value_to_yaml(msg.rssi_at_detection, out);
    out << ", ";
  }

  // member: rssi_at_transmission
  {
    out << "rssi_at_transmission: ";
    rosidl_generator_traits::value_to_yaml(msg.rssi_at_transmission, out);
    out << ", ";
  }

  // member: deferred_relay
  {
    out << "deferred_relay: ";
    rosidl_generator_traits::value_to_yaml(msg.deferred_relay, out);
    out << ", ";
  }

  // member: delay_seconds
  {
    out << "delay_seconds: ";
    rosidl_generator_traits::value_to_yaml(msg.delay_seconds, out);
    out << ", ";
  }

  // member: notes
  {
    out << "notes: ";
    rosidl_generator_traits::value_to_yaml(msg.notes, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VictimAlert & msg,
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

  // member: victim_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "victim_x: ";
    rosidl_generator_traits::value_to_yaml(msg.victim_x, out);
    out << "\n";
  }

  // member: victim_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "victim_y: ";
    rosidl_generator_traits::value_to_yaml(msg.victim_y, out);
    out << "\n";
  }

  // member: rssi_at_detection
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rssi_at_detection: ";
    rosidl_generator_traits::value_to_yaml(msg.rssi_at_detection, out);
    out << "\n";
  }

  // member: rssi_at_transmission
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rssi_at_transmission: ";
    rosidl_generator_traits::value_to_yaml(msg.rssi_at_transmission, out);
    out << "\n";
  }

  // member: deferred_relay
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "deferred_relay: ";
    rosidl_generator_traits::value_to_yaml(msg.deferred_relay, out);
    out << "\n";
  }

  // member: delay_seconds
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "delay_seconds: ";
    rosidl_generator_traits::value_to_yaml(msg.delay_seconds, out);
    out << "\n";
  }

  // member: notes
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "notes: ";
    rosidl_generator_traits::value_to_yaml(msg.notes, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VictimAlert & msg, bool use_flow_style = false)
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
  const resqtether_interfaces::msg::VictimAlert & msg,
  std::ostream & out, size_t indentation = 0)
{
  resqtether_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use resqtether_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const resqtether_interfaces::msg::VictimAlert & msg)
{
  return resqtether_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<resqtether_interfaces::msg::VictimAlert>()
{
  return "resqtether_interfaces::msg::VictimAlert";
}

template<>
inline const char * name<resqtether_interfaces::msg::VictimAlert>()
{
  return "resqtether_interfaces/msg/VictimAlert";
}

template<>
struct has_fixed_size<resqtether_interfaces::msg::VictimAlert>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<resqtether_interfaces::msg::VictimAlert>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<resqtether_interfaces::msg::VictimAlert>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__TRAITS_HPP_

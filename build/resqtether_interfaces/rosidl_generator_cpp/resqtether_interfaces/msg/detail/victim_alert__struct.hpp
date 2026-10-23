// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from resqtether_interfaces:msg/VictimAlert.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "resqtether_interfaces/msg/victim_alert.hpp"


#ifndef RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__STRUCT_HPP_
#define RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__resqtether_interfaces__msg__VictimAlert __attribute__((deprecated))
#else
# define DEPRECATED__resqtether_interfaces__msg__VictimAlert __declspec(deprecated)
#endif

namespace resqtether_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VictimAlert_
{
  using Type = VictimAlert_<ContainerAllocator>;

  explicit VictimAlert_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->victim_x = 0.0;
      this->victim_y = 0.0;
      this->rssi_at_detection = 0.0f;
      this->rssi_at_transmission = 0.0f;
      this->deferred_relay = false;
      this->delay_seconds = 0.0f;
      this->notes = "";
    }
  }

  explicit VictimAlert_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init),
    notes(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->victim_x = 0.0;
      this->victim_y = 0.0;
      this->rssi_at_detection = 0.0f;
      this->rssi_at_transmission = 0.0f;
      this->deferred_relay = false;
      this->delay_seconds = 0.0f;
      this->notes = "";
    }
  }

  // field types and members
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;
  using _victim_x_type =
    double;
  _victim_x_type victim_x;
  using _victim_y_type =
    double;
  _victim_y_type victim_y;
  using _rssi_at_detection_type =
    float;
  _rssi_at_detection_type rssi_at_detection;
  using _rssi_at_transmission_type =
    float;
  _rssi_at_transmission_type rssi_at_transmission;
  using _deferred_relay_type =
    bool;
  _deferred_relay_type deferred_relay;
  using _delay_seconds_type =
    float;
  _delay_seconds_type delay_seconds;
  using _notes_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _notes_type notes;

  // setters for named parameter idiom
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }
  Type & set__victim_x(
    const double & _arg)
  {
    this->victim_x = _arg;
    return *this;
  }
  Type & set__victim_y(
    const double & _arg)
  {
    this->victim_y = _arg;
    return *this;
  }
  Type & set__rssi_at_detection(
    const float & _arg)
  {
    this->rssi_at_detection = _arg;
    return *this;
  }
  Type & set__rssi_at_transmission(
    const float & _arg)
  {
    this->rssi_at_transmission = _arg;
    return *this;
  }
  Type & set__deferred_relay(
    const bool & _arg)
  {
    this->deferred_relay = _arg;
    return *this;
  }
  Type & set__delay_seconds(
    const float & _arg)
  {
    this->delay_seconds = _arg;
    return *this;
  }
  Type & set__notes(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->notes = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    resqtether_interfaces::msg::VictimAlert_<ContainerAllocator> *;
  using ConstRawPtr =
    const resqtether_interfaces::msg::VictimAlert_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<resqtether_interfaces::msg::VictimAlert_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<resqtether_interfaces::msg::VictimAlert_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      resqtether_interfaces::msg::VictimAlert_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<resqtether_interfaces::msg::VictimAlert_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      resqtether_interfaces::msg::VictimAlert_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<resqtether_interfaces::msg::VictimAlert_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<resqtether_interfaces::msg::VictimAlert_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<resqtether_interfaces::msg::VictimAlert_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__resqtether_interfaces__msg__VictimAlert
    std::shared_ptr<resqtether_interfaces::msg::VictimAlert_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__resqtether_interfaces__msg__VictimAlert
    std::shared_ptr<resqtether_interfaces::msg::VictimAlert_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VictimAlert_ & other) const
  {
    if (this->stamp != other.stamp) {
      return false;
    }
    if (this->victim_x != other.victim_x) {
      return false;
    }
    if (this->victim_y != other.victim_y) {
      return false;
    }
    if (this->rssi_at_detection != other.rssi_at_detection) {
      return false;
    }
    if (this->rssi_at_transmission != other.rssi_at_transmission) {
      return false;
    }
    if (this->deferred_relay != other.deferred_relay) {
      return false;
    }
    if (this->delay_seconds != other.delay_seconds) {
      return false;
    }
    if (this->notes != other.notes) {
      return false;
    }
    return true;
  }
  bool operator!=(const VictimAlert_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VictimAlert_

// alias to use template instance with default allocator
using VictimAlert =
  resqtether_interfaces::msg::VictimAlert_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace resqtether_interfaces

#endif  // RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__STRUCT_HPP_

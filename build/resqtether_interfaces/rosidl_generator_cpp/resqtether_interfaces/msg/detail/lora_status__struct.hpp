// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from resqtether_interfaces:msg/LoraStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "resqtether_interfaces/msg/lora_status.hpp"


#ifndef RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__STRUCT_HPP_
#define RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__STRUCT_HPP_

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
# define DEPRECATED__resqtether_interfaces__msg__LoraStatus __attribute__((deprecated))
#else
# define DEPRECATED__resqtether_interfaces__msg__LoraStatus __declspec(deprecated)
#endif

namespace resqtether_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct LoraStatus_
{
  using Type = LoraStatus_<ContainerAllocator>;

  explicit LoraStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sender_id = "";
      this->rssi = 0.0f;
      this->snr = 0.0f;
    }
  }

  explicit LoraStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init),
    sender_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sender_id = "";
      this->rssi = 0.0f;
      this->snr = 0.0f;
    }
  }

  // field types and members
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;
  using _sender_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _sender_id_type sender_id;
  using _rssi_type =
    float;
  _rssi_type rssi;
  using _snr_type =
    float;
  _snr_type snr;

  // setters for named parameter idiom
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }
  Type & set__sender_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->sender_id = _arg;
    return *this;
  }
  Type & set__rssi(
    const float & _arg)
  {
    this->rssi = _arg;
    return *this;
  }
  Type & set__snr(
    const float & _arg)
  {
    this->snr = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    resqtether_interfaces::msg::LoraStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const resqtether_interfaces::msg::LoraStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<resqtether_interfaces::msg::LoraStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<resqtether_interfaces::msg::LoraStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      resqtether_interfaces::msg::LoraStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<resqtether_interfaces::msg::LoraStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      resqtether_interfaces::msg::LoraStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<resqtether_interfaces::msg::LoraStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<resqtether_interfaces::msg::LoraStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<resqtether_interfaces::msg::LoraStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__resqtether_interfaces__msg__LoraStatus
    std::shared_ptr<resqtether_interfaces::msg::LoraStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__resqtether_interfaces__msg__LoraStatus
    std::shared_ptr<resqtether_interfaces::msg::LoraStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LoraStatus_ & other) const
  {
    if (this->stamp != other.stamp) {
      return false;
    }
    if (this->sender_id != other.sender_id) {
      return false;
    }
    if (this->rssi != other.rssi) {
      return false;
    }
    if (this->snr != other.snr) {
      return false;
    }
    return true;
  }
  bool operator!=(const LoraStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LoraStatus_

// alias to use template instance with default allocator
using LoraStatus =
  resqtether_interfaces::msg::LoraStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace resqtether_interfaces

#endif  // RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__STRUCT_HPP_

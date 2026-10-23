// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from resqtether_interfaces:msg/LoraStatus.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "resqtether_interfaces/msg/detail/lora_status__functions.h"
#include "resqtether_interfaces/msg/detail/lora_status__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace resqtether_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void LoraStatus_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) resqtether_interfaces::msg::LoraStatus(_init);
}

void LoraStatus_fini_function(void * message_memory)
{
  auto typed_message = static_cast<resqtether_interfaces::msg::LoraStatus *>(message_memory);
  typed_message->~LoraStatus();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember LoraStatus_message_member_array[4] = {
  {
    "stamp",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<builtin_interfaces::msg::Time>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces::msg::LoraStatus, stamp),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "sender_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces::msg::LoraStatus, sender_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "rssi",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces::msg::LoraStatus, rssi),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "snr",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces::msg::LoraStatus, snr),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers LoraStatus_message_members = {
  "resqtether_interfaces::msg",  // message namespace
  "LoraStatus",  // message name
  4,  // number of fields
  sizeof(resqtether_interfaces::msg::LoraStatus),
  false,  // has_any_key_member_
  LoraStatus_message_member_array,  // message members
  LoraStatus_init_function,  // function to initialize message memory (memory has to be allocated)
  LoraStatus_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t LoraStatus_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &LoraStatus_message_members,
  get_message_typesupport_handle_function,
  &resqtether_interfaces__msg__LoraStatus__get_type_hash,
  &resqtether_interfaces__msg__LoraStatus__get_type_description,
  &resqtether_interfaces__msg__LoraStatus__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace resqtether_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<resqtether_interfaces::msg::LoraStatus>()
{
  return &::resqtether_interfaces::msg::rosidl_typesupport_introspection_cpp::LoraStatus_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, resqtether_interfaces, msg, LoraStatus)() {
  return &::resqtether_interfaces::msg::rosidl_typesupport_introspection_cpp::LoraStatus_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from resqtether_interfaces:msg/LoraStatus.idl
// generated code does not contain a copyright notice
#ifndef RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "resqtether_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "resqtether_interfaces/msg/detail/lora_status__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_resqtether_interfaces
bool cdr_serialize_resqtether_interfaces__msg__LoraStatus(
  const resqtether_interfaces__msg__LoraStatus * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_resqtether_interfaces
bool cdr_deserialize_resqtether_interfaces__msg__LoraStatus(
  eprosima::fastcdr::Cdr &,
  resqtether_interfaces__msg__LoraStatus * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_resqtether_interfaces
size_t get_serialized_size_resqtether_interfaces__msg__LoraStatus(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_resqtether_interfaces
size_t max_serialized_size_resqtether_interfaces__msg__LoraStatus(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_resqtether_interfaces
bool cdr_serialize_key_resqtether_interfaces__msg__LoraStatus(
  const resqtether_interfaces__msg__LoraStatus * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_resqtether_interfaces
size_t get_serialized_size_key_resqtether_interfaces__msg__LoraStatus(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_resqtether_interfaces
size_t max_serialized_size_key_resqtether_interfaces__msg__LoraStatus(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_resqtether_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, resqtether_interfaces, msg, LoraStatus)();

#ifdef __cplusplus
}
#endif

#endif  // RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_

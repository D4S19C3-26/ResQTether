// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from resqtether_interfaces:msg/LoraStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "resqtether_interfaces/msg/lora_status.h"


#ifndef RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__STRUCT_H_
#define RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'sender_id'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/LoraStatus in the package resqtether_interfaces.
/**
  * LoraStatus.msg
 */
typedef struct resqtether_interfaces__msg__LoraStatus
{
  builtin_interfaces__msg__Time stamp;
  rosidl_runtime_c__String sender_id;
  float rssi;
  float snr;
} resqtether_interfaces__msg__LoraStatus;

// Struct for a sequence of resqtether_interfaces__msg__LoraStatus.
typedef struct resqtether_interfaces__msg__LoraStatus__Sequence
{
  resqtether_interfaces__msg__LoraStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} resqtether_interfaces__msg__LoraStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // RESQTETHER_INTERFACES__MSG__DETAIL__LORA_STATUS__STRUCT_H_

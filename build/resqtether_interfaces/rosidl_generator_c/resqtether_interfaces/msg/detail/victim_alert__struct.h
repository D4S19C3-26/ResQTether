// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from resqtether_interfaces:msg/VictimAlert.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "resqtether_interfaces/msg/victim_alert.h"


#ifndef RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__STRUCT_H_
#define RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__STRUCT_H_

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
// Member 'notes'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/VictimAlert in the package resqtether_interfaces.
/**
  * VictimAlert.msg
  * Payload published when a human/victim is identified by the rover.
 */
typedef struct resqtether_interfaces__msg__VictimAlert
{
  builtin_interfaces__msg__Time stamp;
  double victim_x;
  double victim_y;
  float rssi_at_detection;
  float rssi_at_transmission;
  bool deferred_relay;
  float delay_seconds;
  rosidl_runtime_c__String notes;
} resqtether_interfaces__msg__VictimAlert;

// Struct for a sequence of resqtether_interfaces__msg__VictimAlert.
typedef struct resqtether_interfaces__msg__VictimAlert__Sequence
{
  resqtether_interfaces__msg__VictimAlert * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} resqtether_interfaces__msg__VictimAlert__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // RESQTETHER_INTERFACES__MSG__DETAIL__VICTIM_ALERT__STRUCT_H_

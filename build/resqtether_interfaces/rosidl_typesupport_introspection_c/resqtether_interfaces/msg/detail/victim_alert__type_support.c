// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from resqtether_interfaces:msg/VictimAlert.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "resqtether_interfaces/msg/detail/victim_alert__rosidl_typesupport_introspection_c.h"
#include "resqtether_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "resqtether_interfaces/msg/detail/victim_alert__functions.h"
#include "resqtether_interfaces/msg/detail/victim_alert__struct.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/time.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"
// Member `notes`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  resqtether_interfaces__msg__VictimAlert__init(message_memory);
}

void resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_fini_function(void * message_memory)
{
  resqtether_interfaces__msg__VictimAlert__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_message_member_array[8] = {
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces__msg__VictimAlert, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "victim_x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces__msg__VictimAlert, victim_x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "victim_y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces__msg__VictimAlert, victim_y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "rssi_at_detection",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces__msg__VictimAlert, rssi_at_detection),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "rssi_at_transmission",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces__msg__VictimAlert, rssi_at_transmission),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "deferred_relay",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces__msg__VictimAlert, deferred_relay),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "delay_seconds",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces__msg__VictimAlert, delay_seconds),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "notes",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(resqtether_interfaces__msg__VictimAlert, notes),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_message_members = {
  "resqtether_interfaces__msg",  // message namespace
  "VictimAlert",  // message name
  8,  // number of fields
  sizeof(resqtether_interfaces__msg__VictimAlert),
  false,  // has_any_key_member_
  resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_message_member_array,  // message members
  resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_init_function,  // function to initialize message memory (memory has to be allocated)
  resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_message_type_support_handle = {
  0,
  &resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_message_members,
  get_message_typesupport_handle_function,
  &resqtether_interfaces__msg__VictimAlert__get_type_hash,
  &resqtether_interfaces__msg__VictimAlert__get_type_description,
  &resqtether_interfaces__msg__VictimAlert__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_resqtether_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, resqtether_interfaces, msg, VictimAlert)() {
  resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_message_type_support_handle.typesupport_identifier) {
    resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &resqtether_interfaces__msg__VictimAlert__rosidl_typesupport_introspection_c__VictimAlert_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

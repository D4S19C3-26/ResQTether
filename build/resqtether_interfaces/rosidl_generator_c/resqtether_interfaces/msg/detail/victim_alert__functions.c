// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from resqtether_interfaces:msg/VictimAlert.idl
// generated code does not contain a copyright notice
#include "resqtether_interfaces/msg/detail/victim_alert__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"
// Member `notes`
#include "rosidl_runtime_c/string_functions.h"

bool
resqtether_interfaces__msg__VictimAlert__init(resqtether_interfaces__msg__VictimAlert * msg)
{
  if (!msg) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    resqtether_interfaces__msg__VictimAlert__fini(msg);
    return false;
  }
  // victim_x
  // victim_y
  // rssi_at_detection
  // rssi_at_transmission
  // deferred_relay
  // delay_seconds
  // notes
  if (!rosidl_runtime_c__String__init(&msg->notes)) {
    resqtether_interfaces__msg__VictimAlert__fini(msg);
    return false;
  }
  return true;
}

void
resqtether_interfaces__msg__VictimAlert__fini(resqtether_interfaces__msg__VictimAlert * msg)
{
  if (!msg) {
    return;
  }
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
  // victim_x
  // victim_y
  // rssi_at_detection
  // rssi_at_transmission
  // deferred_relay
  // delay_seconds
  // notes
  rosidl_runtime_c__String__fini(&msg->notes);
}

bool
resqtether_interfaces__msg__VictimAlert__are_equal(const resqtether_interfaces__msg__VictimAlert * lhs, const resqtether_interfaces__msg__VictimAlert * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  // victim_x
  if (lhs->victim_x != rhs->victim_x) {
    return false;
  }
  // victim_y
  if (lhs->victim_y != rhs->victim_y) {
    return false;
  }
  // rssi_at_detection
  if (lhs->rssi_at_detection != rhs->rssi_at_detection) {
    return false;
  }
  // rssi_at_transmission
  if (lhs->rssi_at_transmission != rhs->rssi_at_transmission) {
    return false;
  }
  // deferred_relay
  if (lhs->deferred_relay != rhs->deferred_relay) {
    return false;
  }
  // delay_seconds
  if (lhs->delay_seconds != rhs->delay_seconds) {
    return false;
  }
  // notes
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->notes), &(rhs->notes)))
  {
    return false;
  }
  return true;
}

bool
resqtether_interfaces__msg__VictimAlert__copy(
  const resqtether_interfaces__msg__VictimAlert * input,
  resqtether_interfaces__msg__VictimAlert * output)
{
  if (!input || !output) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  // victim_x
  output->victim_x = input->victim_x;
  // victim_y
  output->victim_y = input->victim_y;
  // rssi_at_detection
  output->rssi_at_detection = input->rssi_at_detection;
  // rssi_at_transmission
  output->rssi_at_transmission = input->rssi_at_transmission;
  // deferred_relay
  output->deferred_relay = input->deferred_relay;
  // delay_seconds
  output->delay_seconds = input->delay_seconds;
  // notes
  if (!rosidl_runtime_c__String__copy(
      &(input->notes), &(output->notes)))
  {
    return false;
  }
  return true;
}

resqtether_interfaces__msg__VictimAlert *
resqtether_interfaces__msg__VictimAlert__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  resqtether_interfaces__msg__VictimAlert * msg = (resqtether_interfaces__msg__VictimAlert *)allocator.allocate(sizeof(resqtether_interfaces__msg__VictimAlert), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(resqtether_interfaces__msg__VictimAlert));
  bool success = resqtether_interfaces__msg__VictimAlert__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
resqtether_interfaces__msg__VictimAlert__destroy(resqtether_interfaces__msg__VictimAlert * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    resqtether_interfaces__msg__VictimAlert__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
resqtether_interfaces__msg__VictimAlert__Sequence__init(resqtether_interfaces__msg__VictimAlert__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  resqtether_interfaces__msg__VictimAlert * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(resqtether_interfaces__msg__VictimAlert)) {
      return false;
    }
    data = (resqtether_interfaces__msg__VictimAlert *)allocator.zero_allocate(size, sizeof(resqtether_interfaces__msg__VictimAlert), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = resqtether_interfaces__msg__VictimAlert__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        resqtether_interfaces__msg__VictimAlert__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
resqtether_interfaces__msg__VictimAlert__Sequence__fini(resqtether_interfaces__msg__VictimAlert__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      resqtether_interfaces__msg__VictimAlert__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

resqtether_interfaces__msg__VictimAlert__Sequence *
resqtether_interfaces__msg__VictimAlert__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  resqtether_interfaces__msg__VictimAlert__Sequence * array = (resqtether_interfaces__msg__VictimAlert__Sequence *)allocator.allocate(sizeof(resqtether_interfaces__msg__VictimAlert__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = resqtether_interfaces__msg__VictimAlert__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
resqtether_interfaces__msg__VictimAlert__Sequence__destroy(resqtether_interfaces__msg__VictimAlert__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    resqtether_interfaces__msg__VictimAlert__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
resqtether_interfaces__msg__VictimAlert__Sequence__are_equal(const resqtether_interfaces__msg__VictimAlert__Sequence * lhs, const resqtether_interfaces__msg__VictimAlert__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!resqtether_interfaces__msg__VictimAlert__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
resqtether_interfaces__msg__VictimAlert__Sequence__copy(
  const resqtether_interfaces__msg__VictimAlert__Sequence * input,
  resqtether_interfaces__msg__VictimAlert__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(resqtether_interfaces__msg__VictimAlert)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(resqtether_interfaces__msg__VictimAlert);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    resqtether_interfaces__msg__VictimAlert * data =
      (resqtether_interfaces__msg__VictimAlert *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!resqtether_interfaces__msg__VictimAlert__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          resqtether_interfaces__msg__VictimAlert__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!resqtether_interfaces__msg__VictimAlert__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

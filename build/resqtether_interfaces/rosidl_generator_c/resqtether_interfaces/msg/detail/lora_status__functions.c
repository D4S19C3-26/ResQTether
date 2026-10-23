// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from resqtether_interfaces:msg/LoraStatus.idl
// generated code does not contain a copyright notice
#include "resqtether_interfaces/msg/detail/lora_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"
// Member `sender_id`
#include "rosidl_runtime_c/string_functions.h"

bool
resqtether_interfaces__msg__LoraStatus__init(resqtether_interfaces__msg__LoraStatus * msg)
{
  if (!msg) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    resqtether_interfaces__msg__LoraStatus__fini(msg);
    return false;
  }
  // sender_id
  if (!rosidl_runtime_c__String__init(&msg->sender_id)) {
    resqtether_interfaces__msg__LoraStatus__fini(msg);
    return false;
  }
  // rssi
  // snr
  return true;
}

void
resqtether_interfaces__msg__LoraStatus__fini(resqtether_interfaces__msg__LoraStatus * msg)
{
  if (!msg) {
    return;
  }
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
  // sender_id
  rosidl_runtime_c__String__fini(&msg->sender_id);
  // rssi
  // snr
}

bool
resqtether_interfaces__msg__LoraStatus__are_equal(const resqtether_interfaces__msg__LoraStatus * lhs, const resqtether_interfaces__msg__LoraStatus * rhs)
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
  // sender_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->sender_id), &(rhs->sender_id)))
  {
    return false;
  }
  // rssi
  if (lhs->rssi != rhs->rssi) {
    return false;
  }
  // snr
  if (lhs->snr != rhs->snr) {
    return false;
  }
  return true;
}

bool
resqtether_interfaces__msg__LoraStatus__copy(
  const resqtether_interfaces__msg__LoraStatus * input,
  resqtether_interfaces__msg__LoraStatus * output)
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
  // sender_id
  if (!rosidl_runtime_c__String__copy(
      &(input->sender_id), &(output->sender_id)))
  {
    return false;
  }
  // rssi
  output->rssi = input->rssi;
  // snr
  output->snr = input->snr;
  return true;
}

resqtether_interfaces__msg__LoraStatus *
resqtether_interfaces__msg__LoraStatus__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  resqtether_interfaces__msg__LoraStatus * msg = (resqtether_interfaces__msg__LoraStatus *)allocator.allocate(sizeof(resqtether_interfaces__msg__LoraStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(resqtether_interfaces__msg__LoraStatus));
  bool success = resqtether_interfaces__msg__LoraStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
resqtether_interfaces__msg__LoraStatus__destroy(resqtether_interfaces__msg__LoraStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    resqtether_interfaces__msg__LoraStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
resqtether_interfaces__msg__LoraStatus__Sequence__init(resqtether_interfaces__msg__LoraStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  resqtether_interfaces__msg__LoraStatus * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(resqtether_interfaces__msg__LoraStatus)) {
      return false;
    }
    data = (resqtether_interfaces__msg__LoraStatus *)allocator.zero_allocate(size, sizeof(resqtether_interfaces__msg__LoraStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = resqtether_interfaces__msg__LoraStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        resqtether_interfaces__msg__LoraStatus__fini(&data[i - 1]);
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
resqtether_interfaces__msg__LoraStatus__Sequence__fini(resqtether_interfaces__msg__LoraStatus__Sequence * array)
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
      resqtether_interfaces__msg__LoraStatus__fini(&array->data[i]);
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

resqtether_interfaces__msg__LoraStatus__Sequence *
resqtether_interfaces__msg__LoraStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  resqtether_interfaces__msg__LoraStatus__Sequence * array = (resqtether_interfaces__msg__LoraStatus__Sequence *)allocator.allocate(sizeof(resqtether_interfaces__msg__LoraStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = resqtether_interfaces__msg__LoraStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
resqtether_interfaces__msg__LoraStatus__Sequence__destroy(resqtether_interfaces__msg__LoraStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    resqtether_interfaces__msg__LoraStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
resqtether_interfaces__msg__LoraStatus__Sequence__are_equal(const resqtether_interfaces__msg__LoraStatus__Sequence * lhs, const resqtether_interfaces__msg__LoraStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!resqtether_interfaces__msg__LoraStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
resqtether_interfaces__msg__LoraStatus__Sequence__copy(
  const resqtether_interfaces__msg__LoraStatus__Sequence * input,
  resqtether_interfaces__msg__LoraStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(resqtether_interfaces__msg__LoraStatus)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(resqtether_interfaces__msg__LoraStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    resqtether_interfaces__msg__LoraStatus * data =
      (resqtether_interfaces__msg__LoraStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!resqtether_interfaces__msg__LoraStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          resqtether_interfaces__msg__LoraStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!resqtether_interfaces__msg__LoraStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from resqtether_interfaces:msg/VictimAlert.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "resqtether_interfaces/msg/detail/victim_alert__struct.h"
#include "resqtether_interfaces/msg/detail/victim_alert__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool builtin_interfaces__msg__time__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * builtin_interfaces__msg__time__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool resqtether_interfaces__msg__victim_alert__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[52];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("resqtether_interfaces.msg._victim_alert.VictimAlert", full_classname_dest, 51) == 0);
  }
  resqtether_interfaces__msg__VictimAlert * ros_message = _ros_message;
  {  // stamp
    PyObject * field = PyObject_GetAttrString(_pymsg, "stamp");
    if (!field) {
      return false;
    }
    if (!builtin_interfaces__msg__time__convert_from_py(field, &ros_message->stamp)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // victim_x
    PyObject * field = PyObject_GetAttrString(_pymsg, "victim_x");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->victim_x = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // victim_y
    PyObject * field = PyObject_GetAttrString(_pymsg, "victim_y");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->victim_y = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // rssi_at_detection
    PyObject * field = PyObject_GetAttrString(_pymsg, "rssi_at_detection");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->rssi_at_detection = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // rssi_at_transmission
    PyObject * field = PyObject_GetAttrString(_pymsg, "rssi_at_transmission");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->rssi_at_transmission = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // deferred_relay
    PyObject * field = PyObject_GetAttrString(_pymsg, "deferred_relay");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->deferred_relay = (Py_True == field);
    Py_DECREF(field);
  }
  {  // delay_seconds
    PyObject * field = PyObject_GetAttrString(_pymsg, "delay_seconds");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->delay_seconds = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // notes
    PyObject * field = PyObject_GetAttrString(_pymsg, "notes");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->notes, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * resqtether_interfaces__msg__victim_alert__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of VictimAlert */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("resqtether_interfaces.msg._victim_alert");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "VictimAlert");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  resqtether_interfaces__msg__VictimAlert * ros_message = (resqtether_interfaces__msg__VictimAlert *)raw_ros_message;
  {  // stamp
    PyObject * field = NULL;
    field = builtin_interfaces__msg__time__convert_to_py(&ros_message->stamp);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "stamp", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // victim_x
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->victim_x);
    {
      int rc = PyObject_SetAttrString(_pymessage, "victim_x", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // victim_y
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->victim_y);
    {
      int rc = PyObject_SetAttrString(_pymessage, "victim_y", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // rssi_at_detection
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->rssi_at_detection);
    {
      int rc = PyObject_SetAttrString(_pymessage, "rssi_at_detection", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // rssi_at_transmission
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->rssi_at_transmission);
    {
      int rc = PyObject_SetAttrString(_pymessage, "rssi_at_transmission", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // deferred_relay
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->deferred_relay ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "deferred_relay", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // delay_seconds
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->delay_seconds);
    {
      int rc = PyObject_SetAttrString(_pymessage, "delay_seconds", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // notes
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->notes.data,
      strlen(ros_message->notes.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "notes", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

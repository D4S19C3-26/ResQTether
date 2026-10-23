# generated from rosidl_generator_py/resource/_idl.py.em
# with input from resqtether_interfaces:msg/VictimAlert.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_VictimAlert(type):
    """Metaclass of message 'VictimAlert'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('resqtether_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'resqtether_interfaces.msg.VictimAlert')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__victim_alert
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__victim_alert
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__victim_alert
            cls._TYPE_SUPPORT = module.type_support_msg__msg__victim_alert
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__victim_alert

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class VictimAlert(metaclass=Metaclass_VictimAlert):
    """Message class 'VictimAlert'."""

    __slots__ = [
        '_stamp',
        '_victim_x',
        '_victim_y',
        '_rssi_at_detection',
        '_rssi_at_transmission',
        '_deferred_relay',
        '_delay_seconds',
        '_notes',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'stamp': 'builtin_interfaces/Time',
        'victim_x': 'double',
        'victim_y': 'double',
        'rssi_at_detection': 'float',
        'rssi_at_transmission': 'float',
        'deferred_relay': 'boolean',
        'delay_seconds': 'float',
        'notes': 'string',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from builtin_interfaces.msg import Time
        self.stamp = kwargs.get('stamp', Time())
        self.victim_x = kwargs.get('victim_x', float())
        self.victim_y = kwargs.get('victim_y', float())
        self.rssi_at_detection = kwargs.get('rssi_at_detection', float())
        self.rssi_at_transmission = kwargs.get('rssi_at_transmission', float())
        self.deferred_relay = kwargs.get('deferred_relay', bool())
        self.delay_seconds = kwargs.get('delay_seconds', float())
        self.notes = kwargs.get('notes', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.stamp != other.stamp:
            return False
        if self.victim_x != other.victim_x:
            return False
        if self.victim_y != other.victim_y:
            return False
        if self.rssi_at_detection != other.rssi_at_detection:
            return False
        if self.rssi_at_transmission != other.rssi_at_transmission:
            return False
        if self.deferred_relay != other.deferred_relay:
            return False
        if self.delay_seconds != other.delay_seconds:
            return False
        if self.notes != other.notes:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def stamp(self):
        """Message field 'stamp'."""
        return self._stamp

    @stamp.setter
    def stamp(self, value):
        if self._check_fields:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'stamp' field must be a sub message of type 'Time'"
        self._stamp = value

    @builtins.property
    def victim_x(self):
        """Message field 'victim_x'."""
        return self._victim_x

    @victim_x.setter
    def victim_x(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'victim_x' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'victim_x' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._victim_x = value

    @builtins.property
    def victim_y(self):
        """Message field 'victim_y'."""
        return self._victim_y

    @victim_y.setter
    def victim_y(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'victim_y' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'victim_y' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._victim_y = value

    @builtins.property
    def rssi_at_detection(self):
        """Message field 'rssi_at_detection'."""
        return self._rssi_at_detection

    @rssi_at_detection.setter
    def rssi_at_detection(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'rssi_at_detection' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'rssi_at_detection' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._rssi_at_detection = value

    @builtins.property
    def rssi_at_transmission(self):
        """Message field 'rssi_at_transmission'."""
        return self._rssi_at_transmission

    @rssi_at_transmission.setter
    def rssi_at_transmission(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'rssi_at_transmission' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'rssi_at_transmission' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._rssi_at_transmission = value

    @builtins.property
    def deferred_relay(self):
        """Message field 'deferred_relay'."""
        return self._deferred_relay

    @deferred_relay.setter
    def deferred_relay(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'deferred_relay' field must be of type 'bool'"
        self._deferred_relay = value

    @builtins.property
    def delay_seconds(self):
        """Message field 'delay_seconds'."""
        return self._delay_seconds

    @delay_seconds.setter
    def delay_seconds(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'delay_seconds' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'delay_seconds' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._delay_seconds = value

    @builtins.property
    def notes(self):
        """Message field 'notes'."""
        return self._notes

    @notes.setter
    def notes(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'notes' field must be of type 'str'"
        self._notes = value

// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from resqtether_interfaces:msg/VictimAlert.idl
// generated code does not contain a copyright notice

#include "resqtether_interfaces/msg/detail/victim_alert__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_resqtether_interfaces
const rosidl_type_hash_t *
resqtether_interfaces__msg__VictimAlert__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x63, 0x0d, 0x9d, 0x87, 0x1c, 0x47, 0xa5, 0xc8,
      0x77, 0x96, 0x67, 0xde, 0xce, 0x27, 0x18, 0xf8,
      0x29, 0x5c, 0xa1, 0x84, 0x0d, 0x38, 0x80, 0xf8,
      0x22, 0xd8, 0x2c, 0x8d, 0x8f, 0x31, 0x51, 0x55,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
#endif

static char resqtether_interfaces__msg__VictimAlert__TYPE_NAME[] = "resqtether_interfaces/msg/VictimAlert";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";

// Define type names, field names, and default values
static char resqtether_interfaces__msg__VictimAlert__FIELD_NAME__stamp[] = "stamp";
static char resqtether_interfaces__msg__VictimAlert__FIELD_NAME__victim_x[] = "victim_x";
static char resqtether_interfaces__msg__VictimAlert__FIELD_NAME__victim_y[] = "victim_y";
static char resqtether_interfaces__msg__VictimAlert__FIELD_NAME__rssi_at_detection[] = "rssi_at_detection";
static char resqtether_interfaces__msg__VictimAlert__FIELD_NAME__rssi_at_transmission[] = "rssi_at_transmission";
static char resqtether_interfaces__msg__VictimAlert__FIELD_NAME__deferred_relay[] = "deferred_relay";
static char resqtether_interfaces__msg__VictimAlert__FIELD_NAME__delay_seconds[] = "delay_seconds";
static char resqtether_interfaces__msg__VictimAlert__FIELD_NAME__notes[] = "notes";

static rosidl_runtime_c__type_description__Field resqtether_interfaces__msg__VictimAlert__FIELDS[] = {
  {
    {resqtether_interfaces__msg__VictimAlert__FIELD_NAME__stamp, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
  {
    {resqtether_interfaces__msg__VictimAlert__FIELD_NAME__victim_x, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {resqtether_interfaces__msg__VictimAlert__FIELD_NAME__victim_y, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {resqtether_interfaces__msg__VictimAlert__FIELD_NAME__rssi_at_detection, 17, 17},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {resqtether_interfaces__msg__VictimAlert__FIELD_NAME__rssi_at_transmission, 20, 20},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {resqtether_interfaces__msg__VictimAlert__FIELD_NAME__deferred_relay, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {resqtether_interfaces__msg__VictimAlert__FIELD_NAME__delay_seconds, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {resqtether_interfaces__msg__VictimAlert__FIELD_NAME__notes, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription resqtether_interfaces__msg__VictimAlert__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
resqtether_interfaces__msg__VictimAlert__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {resqtether_interfaces__msg__VictimAlert__TYPE_NAME, 37, 37},
      {resqtether_interfaces__msg__VictimAlert__FIELDS, 8, 8},
    },
    {resqtether_interfaces__msg__VictimAlert__REFERENCED_TYPE_DESCRIPTIONS, 1, 1},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# VictimAlert.msg\n"
  "# Payload published when a human/victim is identified by the rover.\n"
  "builtin_interfaces/Time stamp\n"
  "float64 victim_x\n"
  "float64 victim_y\n"
  "float32 rssi_at_detection\n"
  "float32 rssi_at_transmission\n"
  "bool deferred_relay\n"
  "float32 delay_seconds\n"
  "string notes";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
resqtether_interfaces__msg__VictimAlert__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {resqtether_interfaces__msg__VictimAlert__TYPE_NAME, 37, 37},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 260, 260},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
resqtether_interfaces__msg__VictimAlert__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[2];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 2, 2};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *resqtether_interfaces__msg__VictimAlert__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

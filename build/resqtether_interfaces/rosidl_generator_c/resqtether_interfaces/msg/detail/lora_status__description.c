// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from resqtether_interfaces:msg/LoraStatus.idl
// generated code does not contain a copyright notice

#include "resqtether_interfaces/msg/detail/lora_status__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_resqtether_interfaces
const rosidl_type_hash_t *
resqtether_interfaces__msg__LoraStatus__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xfb, 0x95, 0x0a, 0x3f, 0x4a, 0xc6, 0x05, 0x12,
      0x3c, 0xf5, 0x4d, 0x81, 0x41, 0x00, 0xe2, 0x0f,
      0x35, 0x9a, 0x9a, 0xe8, 0x62, 0xe8, 0x4f, 0x30,
      0xeb, 0xb3, 0x9e, 0x4d, 0x14, 0x5a, 0xbc, 0xc7,
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

static char resqtether_interfaces__msg__LoraStatus__TYPE_NAME[] = "resqtether_interfaces/msg/LoraStatus";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";

// Define type names, field names, and default values
static char resqtether_interfaces__msg__LoraStatus__FIELD_NAME__stamp[] = "stamp";
static char resqtether_interfaces__msg__LoraStatus__FIELD_NAME__sender_id[] = "sender_id";
static char resqtether_interfaces__msg__LoraStatus__FIELD_NAME__rssi[] = "rssi";
static char resqtether_interfaces__msg__LoraStatus__FIELD_NAME__snr[] = "snr";

static rosidl_runtime_c__type_description__Field resqtether_interfaces__msg__LoraStatus__FIELDS[] = {
  {
    {resqtether_interfaces__msg__LoraStatus__FIELD_NAME__stamp, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
  {
    {resqtether_interfaces__msg__LoraStatus__FIELD_NAME__sender_id, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {resqtether_interfaces__msg__LoraStatus__FIELD_NAME__rssi, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {resqtether_interfaces__msg__LoraStatus__FIELD_NAME__snr, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription resqtether_interfaces__msg__LoraStatus__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
resqtether_interfaces__msg__LoraStatus__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {resqtether_interfaces__msg__LoraStatus__TYPE_NAME, 36, 36},
      {resqtether_interfaces__msg__LoraStatus__FIELDS, 4, 4},
    },
    {resqtether_interfaces__msg__LoraStatus__REFERENCED_TYPE_DESCRIPTIONS, 1, 1},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# LoraStatus.msg\n"
  "builtin_interfaces/Time stamp\n"
  "string sender_id\n"
  "float32 rssi\n"
  "float32 snr";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
resqtether_interfaces__msg__LoraStatus__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {resqtether_interfaces__msg__LoraStatus__TYPE_NAME, 36, 36},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 89, 89},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
resqtether_interfaces__msg__LoraStatus__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[2];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 2, 2};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *resqtether_interfaces__msg__LoraStatus__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

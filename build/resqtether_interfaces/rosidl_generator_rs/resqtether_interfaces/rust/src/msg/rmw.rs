#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "resqtether_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__resqtether_interfaces__msg__LoraStatus() -> *const std::ffi::c_void;
}

#[link(name = "resqtether_interfaces__rosidl_generator_c")]
extern "C" {
    fn resqtether_interfaces__msg__LoraStatus__init(msg: *mut LoraStatus) -> bool;
    fn resqtether_interfaces__msg__LoraStatus__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LoraStatus>, size: usize) -> bool;
    fn resqtether_interfaces__msg__LoraStatus__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LoraStatus>);
    fn resqtether_interfaces__msg__LoraStatus__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LoraStatus>, out_seq: *mut rosidl_runtime_rs::Sequence<LoraStatus>) -> bool;
}

// Corresponds to resqtether_interfaces__msg__LoraStatus
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// LoraStatus.msg

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LoraStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sender_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rssi: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub snr: f32,

}



impl Default for LoraStatus {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !resqtether_interfaces__msg__LoraStatus__init(&mut msg as *mut _) {
        panic!("Call to resqtether_interfaces__msg__LoraStatus__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LoraStatus {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { resqtether_interfaces__msg__LoraStatus__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { resqtether_interfaces__msg__LoraStatus__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { resqtether_interfaces__msg__LoraStatus__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LoraStatus {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LoraStatus where Self: Sized {
  const TYPE_NAME: &'static str = "resqtether_interfaces/msg/LoraStatus";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__resqtether_interfaces__msg__LoraStatus() }
  }
}


#[link(name = "resqtether_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__resqtether_interfaces__msg__VictimAlert() -> *const std::ffi::c_void;
}

#[link(name = "resqtether_interfaces__rosidl_generator_c")]
extern "C" {
    fn resqtether_interfaces__msg__VictimAlert__init(msg: *mut VictimAlert) -> bool;
    fn resqtether_interfaces__msg__VictimAlert__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<VictimAlert>, size: usize) -> bool;
    fn resqtether_interfaces__msg__VictimAlert__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<VictimAlert>);
    fn resqtether_interfaces__msg__VictimAlert__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<VictimAlert>, out_seq: *mut rosidl_runtime_rs::Sequence<VictimAlert>) -> bool;
}

// Corresponds to resqtether_interfaces__msg__VictimAlert
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// VictimAlert.msg
/// Payload published when a human/victim is identified by the rover.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct VictimAlert {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub victim_x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub victim_y: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rssi_at_detection: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rssi_at_transmission: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub deferred_relay: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub delay_seconds: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub notes: rosidl_runtime_rs::String,

}



impl Default for VictimAlert {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !resqtether_interfaces__msg__VictimAlert__init(&mut msg as *mut _) {
        panic!("Call to resqtether_interfaces__msg__VictimAlert__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for VictimAlert {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { resqtether_interfaces__msg__VictimAlert__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { resqtether_interfaces__msg__VictimAlert__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { resqtether_interfaces__msg__VictimAlert__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for VictimAlert {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for VictimAlert where Self: Sized {
  const TYPE_NAME: &'static str = "resqtether_interfaces/msg/VictimAlert";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__resqtether_interfaces__msg__VictimAlert() }
  }
}



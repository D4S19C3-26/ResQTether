#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to resqtether_interfaces__msg__LoraStatus
/// LoraStatus.msg

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LoraStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sender_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rssi: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub snr: f32,

}



impl Default for LoraStatus {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::LoraStatus::default())
  }
}

impl rosidl_runtime_rs::Message for LoraStatus {
  type RmwMsg = super::msg::rmw::LoraStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
        sender_id: msg.sender_id.as_str().into(),
        rssi: msg.rssi,
        snr: msg.snr,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
        sender_id: msg.sender_id.as_str().into(),
      rssi: msg.rssi,
      snr: msg.snr,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
      sender_id: msg.sender_id.to_string(),
      rssi: msg.rssi,
      snr: msg.snr,
    }
  }
}


// Corresponds to resqtether_interfaces__msg__VictimAlert
/// VictimAlert.msg
/// Payload published when a human/victim is identified by the rover.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct VictimAlert {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,


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
    pub notes: std::string::String,

}



impl Default for VictimAlert {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::VictimAlert::default())
  }
}

impl rosidl_runtime_rs::Message for VictimAlert {
  type RmwMsg = super::msg::rmw::VictimAlert;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
        victim_x: msg.victim_x,
        victim_y: msg.victim_y,
        rssi_at_detection: msg.rssi_at_detection,
        rssi_at_transmission: msg.rssi_at_transmission,
        deferred_relay: msg.deferred_relay,
        delay_seconds: msg.delay_seconds,
        notes: msg.notes.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      victim_x: msg.victim_x,
      victim_y: msg.victim_y,
      rssi_at_detection: msg.rssi_at_detection,
      rssi_at_transmission: msg.rssi_at_transmission,
      deferred_relay: msg.deferred_relay,
      delay_seconds: msg.delay_seconds,
        notes: msg.notes.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
      victim_x: msg.victim_x,
      victim_y: msg.victim_y,
      rssi_at_detection: msg.rssi_at_detection,
      rssi_at_transmission: msg.rssi_at_transmission,
      deferred_relay: msg.deferred_relay,
      delay_seconds: msg.delay_seconds,
      notes: msg.notes.to_string(),
    }
  }
}



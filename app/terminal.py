from clock import *
from power import *

DISCHARGING = "Discharging"
CHARGING = "Charging"
BATTERY_ERROR = "Error. Can't read battery state."
BATTERY_STATUS = "%s, Battery charge: %s, %s. %s"
MESSAGE_RESET = ""
CONNECT_CHARGER = "Please plug the charger in."
DISCONNECT_CHARGER = "Please disconnect the charger."
STAGE_DONE = "Stage %d done."

def stage_done(stage_number):
    return STAGE_DONE % (stage_number)

def status_reset():
    return MESSAGE_RESET

def disconnect_charger():
    return DISCONNECT_CHARGER

def connect_charger():
    return CONNECT_CHARGER

def print_status(message_text):
    power_state = DISCHARGING
    timestamp = format_time(current_time())
    charge_percent = check_battery_charge()

    power_cable_is_connected = is_power_cable_connected()
    if power_cable_is_connected:
        power_state = CHARGING
    elif power_cable_is_connected is None:
        power_state = BATTERY_ERROR

    print(BATTERY_STATUS % (timestamp, charge_percent, power_state, message_text))
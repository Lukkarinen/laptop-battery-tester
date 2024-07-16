import sounds, power, clock

#region Terminal
DISCHARGING = "Discharging"
CHARGING = "Charging"
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
    timestamp = clock.format_time(clock.current_time())
    charge_percent = power.check_battery_charge()
    power_state = DISCHARGING
    if power.is_power_cable_connected():
        power_state = CHARGING
    print(BATTERY_STATUS % (timestamp, charge_percent, power_state, message_text))
#endregion

FIRST_CHARGE = 1
DISCHARGE = 2
SECOND_CHARGE = 3
TEST_END = 4

PRESS_ENTER = "Press Enter to end program..."

def main():
    sound_on = sounds.mute_sound()
    stage = FIRST_CHARGE
    last_alarm = clock.current_time()

    while stage != TEST_END:
        frame_start = clock.current_time()
        status_message = status_reset()

        battery_full = power.is_battery_full()
        battery_empty = power.is_battery_empty()
        power_cable_connected = power.is_power_cable_connected()

        if stage == FIRST_CHARGE or stage == SECOND_CHARGE:
            if battery_full:
                status_message = stage_done(stage)
                stage += 1
            elif not power_cable_connected and power_cable_connected is not None:
                status_message = connect_charger()
                if sound_on and clock.has_it_been_long_enough(last_alarm):
                    sounds.play_alarm()
                    last_alarm = clock.current_time()

        elif stage == DISCHARGE:
            if battery_empty:
                status_message = stage_done(stage)
                stage += 1
            elif power_cable_connected:
                status_message = disconnect_charger()
        
        print_status(status_message)
        clock.sleep(frame_start)
    
    if sound_on:
        sounds.play_alarm()

    input(PRESS_ENTER)

main()
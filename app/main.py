from terminal import *
from sounds import ask_to_enable_sound, play_alarm

FIRST_CHARGE = 1
DISCHARGE = 2
SECOND_CHARGE = 3
TEST_END = 4

PRESS_ENTER = "Press Enter to end program..."

def main():
    sound_on = ask_to_enable_sound()
    stage = FIRST_CHARGE
    last_alarm = current_time()

    while stage != TEST_END:
        frame_start = current_time()
        status_message = status_reset()

        battery_full = is_battery_full()
        battery_empty = is_battery_empty()
        power_cable_connected = is_power_cable_connected()

        if stage == FIRST_CHARGE or stage == SECOND_CHARGE:
            if battery_full:
                status_message = stage_done(stage)
                stage += 1
            elif not power_cable_connected and power_cable_connected is not None:
                status_message = connect_charger()
                if sound_on and has_it_been_long_enough(last_alarm):
                    play_alarm()
                    last_alarm = current_time()

        elif stage == DISCHARGE:
            if battery_empty:
                status_message = stage_done(stage)
                stage += 1
            elif power_cable_connected:
                status_message = disconnect_charger()
        
        print_status(status_message)
        sleep_until_next_frame(frame_start)
    
    if sound_on:
        play_alarm()

    input(PRESS_ENTER)

main()
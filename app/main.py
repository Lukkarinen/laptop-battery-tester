from terminal import Terminal
from sounds import Alarm
from power import Battery
from datetime import datetime
import time

def sleep_until_next_frame(frame_start, refresh_rate = 0.1):
    seconds_since_frame_start = (datetime.now() - frame_start).total_seconds()

    if seconds_since_frame_start < refresh_rate and seconds_since_frame_start > 0:
        sleep_duration = refresh_rate - seconds_since_frame_start
        time.sleep(sleep_duration)
        return True
    else:
        return False

FIRST_CHARGE = 1
DISCHARGE = 2
SECOND_CHARGE = 3
TEST_END = 4

def main():
    alarm = Alarm()
    battery = Battery()
    terminal = Terminal()
    stage = FIRST_CHARGE

    alarm.alarm()

    while stage != TEST_END:
        frame_start = datetime.now()

        battery.full = battery.is_full()
        battery.empty = battery.is_empty()
        battery.charging = battery.is_charging()
        battery.charge = battery.check_charge()

        event = "none"

        if battery.charging is None or battery.charge == -1:
            event = "error"
            alarm.alarm()

        elif stage == FIRST_CHARGE or stage == SECOND_CHARGE:
            if battery.full:
                event = "stage"
            elif not battery.charging and battery.charging is not None:
                event = "connect"
                alarm.alarm()

        elif stage == DISCHARGE:
            if battery.empty:
                event = "stage"
            elif battery.charging:
                event = "disconnect"
                alarm.alarm()
    
        terminal.print_status(datetime.now(), battery.charge, battery.charging, event, stage)

        if event == "stage":
            stage += 1

        sleep_until_next_frame(frame_start)
    

    alarm.alarm()
    terminal.input_enter()

if __name__ == '__main__':
    main()
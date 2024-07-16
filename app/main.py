#region Imports
import psutil
import time
from datetime import datetime
import playsound
import pathlib
#endregion

#region Time
TIMESTAMP_FORMAT = "%d.%m.%Y, %H:%M:%S"
REFRESH_RATE = 0.33 #Seconds
BEEP_INTERVAL = 3 #Seconds between alarm beeps
BACK_TO_THE_FUTURE = "Time difference is negative. Either something went wrong or the user traveled back in time"

def current_time():
    return datetime.now()

def format_time(timestamp):
    #Format a time object into a single string that's more suitable for writing into a dumb database or printing into terminal
    return timestamp.strftime(TIMESTAMP_FORMAT)

def sleep(frame_start_time):
    seconds_since_frame_start = (current_time() - frame_start_time).total_seconds()
    if seconds_since_frame_start < REFRESH_RATE:
        sleep_duration = REFRESH_RATE - seconds_since_frame_start
        time.sleep(sleep_duration)
        return True
    else:
        return False
    
def has_it_been_long_enough(last_time):
    time_difference = (current_time() - last_time).total_seconds()
    if time_difference < 0:
        log_error(BACK_TO_THE_FUTURE)
        return False
    elif time_difference >= BEEP_INTERVAL:
        return True
    else:
        return False
#endregion

#region Power
BATTERY_HIGH_THRESHOLD = 95 #At or above this percent, the battery is considered full
BATTERY_LOW_THRESHOLD = 5 #At or below this percent, the battery is considered empty
BATTERY_ERROR_RETURN_VALUE = -1 #If battery charge can't be read, return -1
CHARGER_ERROR_RETURN_VALUE = None #If the battery's metrics can't be read or access to read the battery's state is denied, return None

BATTERY_ACCESS_DENIED_ERROR = "Tried to read battery charge percent, but access was denied"
CHARGER_ACCESS_DENIED_ERROR = "Tried to read power cable state, but access was denied"
BATTERY_READ_ERROR = "No battery installed or battery metrics can't be read"

def check_battery_charge():
    try:
        charge = psutil.sensors_battery().percent
    except psutil.AccessDenied:
        log_error(BATTERY_ACCESS_DENIED_ERROR)
        return BATTERY_ERROR_RETURN_VALUE
    if charge is None:
        log_error(BATTERY_READ_ERROR)
        return BATTERY_ERROR_RETURN_VALUE
    else:
        return charge
    
def is_battery_full():
    if check_battery_charge() >= BATTERY_HIGH_THRESHOLD:
        return True
    else:
        return False
    
def is_battery_empty():
    charge = check_battery_charge()
    if charge == BATTERY_ERROR_RETURN_VALUE:
        return False
    elif charge <= BATTERY_LOW_THRESHOLD:
        return True
    else:
        return False

def is_power_cable_connected():
    try:
        charging = psutil.sensors_battery().power_plugged
    except psutil.AccessDenied:
        log_error(CHARGER_ACCESS_DENIED_ERROR)
        return CHARGER_ERROR_RETURN_VALUE
    if charging is None:
        log_error(BATTERY_READ_ERROR)
        return CHARGER_ERROR_RETURN_VALUE
    else:
        return charging
#endregion

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
    timestamp = format_time(datetime.now())
    charge_percent = check_battery_charge()
    power_state = DISCHARGING
    if is_power_cable_connected():
        power_state = CHARGING
    print(BATTERY_STATUS % (timestamp, charge_percent, power_state, message_text))
#endregion

#region Sound
SOUND_FILE = "\\sound\\beep.mp3"
SOUND_FILE_NOT_FOUND = "Sound file not found: %s"
DEFAULT_SOUND_SETTING = False
SOUND_PERMISSION = "Do you want the program to play sound when it needs your attention? y/n"

def running_path():
    return pathlib.Path(__file__).parent.resolve()

def play_alarm():
    soundfile = str(running_path()) + SOUND_FILE
    try:
        playsound.playsound(soundfile)
    except playsound.PlaysoundException:
        log_error(SOUND_FILE_NOT_FOUND % soundfile)
        print('\a')

def set_sound_permission():
    try:
        is_okay = input(SOUND_PERMISSION).lower().strip() == "y"
        if is_okay:
            return True
        else:
            return False
    except ValueError:
        return DEFAULT_SOUND_SETTING
#endregion

#region Errors
NO_ERRORS = "There were no errors during the test."
ERROR_LINE = "%d times %s"
list_of_errors = {}

def log_error(error_text):
    print(error_text)
    if error_text in list_of_errors:
        list_of_errors[error_text] = list_of_errors[error_text] +1
    else:
        list_of_errors.update({error_text : 1})

def print_error_statistics():
    error_list_is_not_empty = bool(list_of_errors)
    if error_list_is_not_empty:
        for error in list_of_errors:
            amount = list_of_errors[error]
            print(ERROR_LINE % (amount, error))
    else:
        print(NO_ERRORS)
#endregion

FIRST_CHARGE = 1
DISCHARGE = 2
SECOND_CHARGE = 3
TEST_END = 4

PRESS_ENTER = "Press Enter to end program..."

def main():
    sound_on = set_sound_permission()
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
        sleep(frame_start)
    
    if sound_on:
        play_alarm()

    print_error_statistics()
    input(PRESS_ENTER)

main()
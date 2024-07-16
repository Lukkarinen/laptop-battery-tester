from datetime import datetime
import time

TIMESTAMP_FORMAT = "%d.%m.%Y, %H:%M:%S"
REFRESH_RATE = 0.33 #Seconds
BEEP_INTERVAL = 3 #Seconds between alarm beeps
BACK_TO_THE_FUTURE = "Time difference is negative. Either something went wrong or the user traveled back in time"

def current_time():
    return datetime.now()

def format_time(timestamp):
    #Format a time object into a single string that's more suitable for writing into a dumb database or printing into terminal
    return timestamp.strftime(TIMESTAMP_FORMAT)

def sleep_until_next_frame(frame_start_time):
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
        return False
    elif time_difference >= BEEP_INTERVAL:
        return True
    else:
        return False
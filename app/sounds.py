import pathlib
import playsound

SOUND_FILE = "\\sound\\beep.mp3"
DEFAULT_MUTE_SETTING = True
SOUND_PERMISSION = "Do you want the program to play sound when it needs your attention? y/n"

def running_path():
    return pathlib.Path(__file__).parent.resolve()

def play_alarm():
    sound_file = str(running_path()) + SOUND_FILE
    try:
        playsound.playsound(sound_file)
    except playsound.PlaysoundException as error:
        print(error)
        print('\a') #This should work on all platforms and play a "bell" sound as long as the terminal isn't muted

def ask_to_enable_sound():
    try:
        is_okay = input(SOUND_PERMISSION).lower().strip() == "y"
        if is_okay:
            return True
        else:
            return False
    except:
        return DEFAULT_MUTE_SETTING
import pathlib
import playsound
from datetime import datetime, timedelta
import multiprocessing

class Alarm:
    def __init__(self,
                 sound_file = "\\sound\\beep.mp3",
                 mute = True,
                 alarm_interval = 3
                 ):
        
        self.file_path = self.sound_file_path(sound_file)
        self.mute = mute
        self.last_alarm = None
        self.too_soon = False
        self.alarm_interval = alarm_interval
        
    def running_path(self):
        return pathlib.Path(__file__).parent.resolve()

    def sound_file_path(self, sound_file):
        return str(self.running_path()) + sound_file

    def play_alarm(self):
        try:
            playsound.playsound(self.file_path)
        except (playsound.PlaysoundException, FileNotFoundError) as error:
            print(error)
            print('\a') #This should play a "bell" sound on all operating systems as long as the terminal isn't muted
        
    def alarm(self):
        too_soon = self.is_it_too_soon()
        if not too_soon:
            self.last_alarm = datetime.now()
            try:
                process = multiprocessing.Process(target = self.play_alarm)
                process.start()
            except RuntimeError as error:
                print(error)

    def is_it_too_soon(self):
        if self.last_alarm is not None:
            seconds_since_last_alarm = (datetime.now() - self.last_alarm).total_seconds()
            if seconds_since_last_alarm >= self.alarm_interval:
                return False
            else:
                return True
        else:
            return False
#region Imports
from psutil import sensors_battery, AccessDenied
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

def currentTime():
    return datetime.now()

def formatTime(timestamp):
    #Format a time object into a single string that's more suitable for writing into a dumb database or printing into terminal
    return timestamp.strftime(TIMESTAMP_FORMAT)

def sleep(frameStartTime):
    secondsSinceFrameStart = (currentTime() - frameStartTime).total_seconds()
    if secondsSinceFrameStart < REFRESH_RATE:
        sleepDuration = REFRESH_RATE - secondsSinceFrameStart
        time.sleep(sleepDuration)
        return True
    else:
        return False
    
def hasItBeenLongEnough(lastTime):
    timeDifference = (currentTime() - lastTime).total_seconds()
    if timeDifference < 0:
        logError(BACK_TO_THE_FUTURE)
        return False
    elif timeDifference >= BEEP_INTERVAL:
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

def checkBatteryCharge():
    try:
        charge = sensors_battery().percent
    except AccessDenied:
        logError(BATTERY_ACCESS_DENIED_ERROR)
        return BATTERY_ERROR_RETURN_VALUE
    if charge is None:
        logError(BATTERY_READ_ERROR)
        return BATTERY_ERROR_RETURN_VALUE
    else:
        return charge
    
def isBatteryFull():
    if checkBatteryCharge() >= BATTERY_HIGH_THRESHOLD:
        return True
    else:
        return False
    
def isBatteryEmpty():
    charge = checkBatteryCharge()
    if charge == BATTERY_ERROR_RETURN_VALUE:
        return False
    elif charge <= BATTERY_LOW_THRESHOLD:
        return True
    else:
        return False

def isPowerCableConnected():
    try:
        charging = sensors_battery().power_plugged
    except AccessDenied:
        logError(CHARGER_ACCESS_DENIED_ERROR)
        return CHARGER_ERROR_RETURN_VALUE
    if charging is None:
        logError(BATTERY_READ_ERROR)
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

def stageDone(stageNum):
    return STAGE_DONE % (stageNum)

def statusReset():
    return MESSAGE_RESET

def disconnectCharger():
    return DISCONNECT_CHARGER

def connectCharger():
    return CONNECT_CHARGER

def printStatus(messageText):
    timestamp = formatTime(datetime.now())
    chargePercent = checkBatteryCharge()
    powerState = DISCHARGING
    if isPowerCableConnected():
        powerState = CHARGING
    print(BATTERY_STATUS % (timestamp, chargePercent, powerState, messageText))
#endregion

#region Sound
SOUND_FILE = "\\sound\\beep.mp3"
SOUND_FILE_NOT_FOUND = "Sound file not found: %s"
DEFAULT_SOUND_SETTING = False
SOUND_PERMISSION = "Do you want the program to play sound when it needs your attention? y/n"

def runningPath():
    return pathlib.Path(__file__).parent.resolve()

def playAlarm():
    soundfile = str(runningPath()) + SOUND_FILE
    try:
        playsound.playsound(soundfile)
    except playsound.PlaysoundException:
        logError(SOUND_FILE_NOT_FOUND % soundfile)
        print('\a')

def setSoundPermission():
    try:
        isOkay = input(SOUND_PERMISSION).lower().strip() == "y"
        if isOkay:
            return True
        else:
            return False
    except ValueError:
        return DEFAULT_SOUND_SETTING
#endregion

#region Errors
NO_ERRORS = "There were no errors during the test."
ERROR_LINE = "%d times %s"
listOfErrors = {}

def logError(errortext):
    print(errortext)
    if errortext in listOfErrors:
        listOfErrors[errortext] = listOfErrors[errortext] +1
    else:
        listOfErrors.update({errortext : 1})

def printErrorStatistics():
    errorListIsNotEmpty = bool(listOfErrors)
    if errorListIsNotEmpty:
        for error in listOfErrors:
            amount = listOfErrors[error]
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
    soundOn = setSoundPermission()
    stage = FIRST_CHARGE
    lastAlarm = currentTime()

    while stage != TEST_END:
        frameStartTime = currentTime()
        statusMessage = statusReset()

        batteryFull = isBatteryFull()
        batteryEmpty = isBatteryEmpty()
        powerCableConnected = isPowerCableConnected()

        if stage == FIRST_CHARGE or stage == SECOND_CHARGE:
            if batteryFull:
                statusMessage = stageDone(stage)
                stage += 1
            elif not powerCableConnected and powerCableConnected is not None:
                statusMessage = connectCharger()
                if soundOn and hasItBeenLongEnough(lastAlarm):
                    playAlarm()
                    lastAlarm = currentTime()

        elif stage == DISCHARGE:
            if batteryEmpty:
                statusMessage = stageDone(stage)
                stage += 1
            elif powerCableConnected:
                statusMessage = disconnectCharger()
        
        printStatus(statusMessage)
        sleep(frameStartTime)
    
    if soundOn:
        playAlarm()

    printErrorStatistics()
    input(PRESS_ENTER)

main()
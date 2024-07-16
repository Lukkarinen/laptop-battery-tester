import psutil

BATTERY_HIGH_THRESHOLD = 95 #At or above this percent, the battery is considered full
BATTERY_LOW_THRESHOLD = 5 #At or below this percent, the battery is considered empty
BATTERY_ERROR = -1 #If battery charge can't be read, return -1
CHARGER_ERROR = None #If the battery's metrics can't be read or access to read the battery's state is denied, return None

def check_battery_charge():
    try:
        charge = psutil.sensors_battery().percent
    except (psutil.AccessDenied, AttributeError) as error:
        return BATTERY_ERROR
    if charge is None or charge < 0 or charge > 200:
        return BATTERY_ERROR
    else:
        return charge
    
def is_battery_full():
    if check_battery_charge() >= BATTERY_HIGH_THRESHOLD:
        return True
    else:
        return False
    
def is_battery_empty():
    charge = check_battery_charge()
    if charge == BATTERY_ERROR:
        return False
    elif charge <= BATTERY_LOW_THRESHOLD:
        return True
    else:
        return False

def is_power_cable_connected():
    try:
        charging = psutil.sensors_battery().power_plugged
    except (AttributeError, psutil.AccessDenied) as error:
        return CHARGER_ERROR
    return charging
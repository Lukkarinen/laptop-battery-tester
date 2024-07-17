import psutil

class Battery:
    def __init__(self, 
                 battery_high_threshold = 95,
                 battery_low_threshold = 5,
                 battery_error = -1,
                 charger_error = None
                 ):
        
        self.battery_high_threshold = battery_high_threshold
        self.battery_low_threshold = battery_low_threshold
        self.battery_error = battery_error
        self.charger_error = charger_error
        self.full = self.is_full()
        self.empty = self.is_empty()
        self.charging = self.is_charging()
        self.charge = self.check_charge()

    def check_charge(self):
        try:
            charge = psutil.sensors_battery().percent
        except (psutil.AccessDenied, AttributeError) as error:
            print(error)
            return self.battery_error
        if charge is None or charge < 0 or charge > 110:
            return self.battery_error
        else:
            return charge
    
    def is_full(self):
        if self.check_charge() >= self.battery_high_threshold:
            return True
        else:
            return False
    
    def is_empty(self):
        charge = self.check_charge()
        if charge == self.battery_error:
            return False
        elif charge <= self.battery_low_threshold:
            return True
        else:
            return False

    def is_charging(self):
        try:
            charging = psutil.sensors_battery().power_plugged
        except (AttributeError, psutil.AccessDenied) as error:
            print(error)
            return self.charger_error
        return charging
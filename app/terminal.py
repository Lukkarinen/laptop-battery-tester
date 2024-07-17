class Terminal:
    def __init__(self,
                 timestamp_format = "%d.%m.%Y, %H:%M:%S", #days.months.years, hours:minutes:seconds, example: 17.07.2024, 13:11:45
                 discharging = "Discharging",
                 charging = "Charging",
                 battery_error = "Error: Can't read battery state",
                 battery_charge = "Battery charge",
                 connect_charger = "Please plug the charger in",
                 disconnect_charger = "Please disconnect the charger",
                 stage_done = "Stage %s done",
                 press_enter = "Press Enter to end the program..."
                 ):
        
        self.timestamp_format = timestamp_format
        self.discharging = discharging
        self.charging = charging
        self.battery_error = battery_error
        self.battery_charge = battery_charge
        self.connect_charger = connect_charger
        self.disconnect_charger = disconnect_charger
        self.stage_done = stage_done
        self.press_enter = press_enter

    def format_timestamp(self, timestamp):
        #Format a time object into a single string that's more suitable for writing into a dumb database or printing into terminal
        return timestamp.strftime(self.timestamp_format)
    
    def format_stage(self, stage):
        return self.stage_done % str(stage)
    
    def charging_or_discharging(self, charging):
        if charging:
            return self.charging
        else:
            return self.discharging
    
    def input_enter(self):
        input(self.press_enter)
        
    def print_status(self, timestamp, charge_percent, charging_state, event, stage=1):
        formatted_timestamp = self.format_timestamp(timestamp)

        charging = self.charging_or_discharging(charging_state)

        match event:
            case "stage":
                message_text = self.format_stage(stage)
            case "disconnect":
                message_text = self.disconnect_charger
            case "connect":
                message_text = self.connect_charger
            case "error":
                message_text = self.battery_error
            case _:
                message_text = ""

        print("%s, %s: %d, %s. %s" % (formatted_timestamp, self.battery_charge, charge_percent, charging, message_text))
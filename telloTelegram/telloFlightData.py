class FlightData():
    
    def __init__(self):
        self.battery_low = 0
        self.battery_lower = 0
        self.battery_percentage = 0
        self.battery_state = 0
        self.camera_state = 0
        self.down_visual_state = 0
        self.drone_battery_left = 0
        self.drone_fly_time_left = 0
        self.drone_hover = 0
        self.em_open = 0
        self.em_sky = 0
        self.em_ground = 0
        self.east_speed = 0
        self.electrical_machinery_state = 0
        self.factory_mode = 0
        self.fly_mode = 0
        self.fly_speed = 0
        self.fly_time = 0
        self.front_in = 0
        self.front_lsc = 0
        self.front_out = 0
        self.gravity_state = 0
        self.ground_speed = 0
        self.height = 0
        self.imu_calibration_state = 0
        self.imu_state = 0
        self.light_strength = 0
        self.north_speed = 0
        self.outage_recording = 0
        self.power_state = 0
        self.pressure_state = 0
        self.smart_video_exit_mode = 0
        self.temperature_height = 0
        self.throw_fly_timer = 0
        self.wifi_disturb = 0
        self.wifi_strength = 0
        self.wind_state = 0
        
    def getData(self, data):

        if len(data) < 24:
            return ""

        self.height = int.from_bytes(data[0:1], "little") #int16(data[0], data[1])
        self.north_speed = int.from_bytes(data[2:3], "little")# int16(data[2], data[3])
        self.east_speed = int.from_bytes(data[4:5], "little") # int16(data[4], data[5])
        self.ground_speed = int.from_bytes(data[7:7], "little")# int16(data[6], data[7])
        self.fly_time = int.from_bytes(data[8:9], "little") #int16(data[8], data[9])

        self.imu_state = ((data[10] >> 0) & 0x1)
        self.pressure_state = ((data[10] >> 1) & 0x1)
        self.down_visual_state = ((data[10] >> 2) & 0x1)
        self.power_state = ((data[10] >> 3) & 0x1)
        self.battery_state = ((data[10] >> 4) & 0x1)
        self.gravity_state = ((data[10] >> 5) & 0x1)
        self.wind_state = ((data[10] >> 7) & 0x1)

        self.imu_calibration_state = data[11]
        self.battery_percentage = data[12]
        self.drone_battery_left = int.from_bytes(data[13:14], "little") #int16(data[13], data[14])
        self.drone_fly_time_left = int.from_bytes(data[15:16], "little") #int16(data[15], data[16])

        self.em_sky = ((data[17] >> 0) & 0x1)
        self.em_ground = ((data[17] >> 1) & 0x1)
        self.em_open = ((data[17] >> 2) & 0x1)
        self.drone_hover = ((data[17] >> 3) & 0x1)
        self.outage_recording = ((data[17] >> 4) & 0x1)
        self.battery_low = ((data[17] >> 5) & 0x1)
        self.battery_lower = ((data[17] >> 6) & 0x1)
        self.factory_mode = ((data[17] >> 7) & 0x1)

        self.fly_mode = data[18]
        self.throw_fly_timer = data[19]
        self.camera_state = data[20]
        self.electrical_machinery_state = data[21]

        self.front_in = ((data[22] >> 0) & 0x1)
        self.front_out = ((data[22] >> 1) & 0x1)
        self.front_lsc = ((data[22] >> 2) & 0x1)

        self.temperature_height = ((data[23] >> 0) & 0x1)
        #
        return (
            ("ALT: %2d" % self.height) +
            (" | SPD: %2d" % self.ground_speed) +
            (" | BAT: %2d" % self.battery_percentage) +
            (" | WIFI: %2d" % self.wifi_strength) +
            (" | CAM: %2d" % self.camera_state) +
            (" | MODE: %2d" % self.fly_mode) +
            # (", drone_battery_left=0x%04x" % self.drone_battery_left) +
            "")
if __name__ == '__main__':
    print('Later you can use temptest.py not implemented yet (for testing.)')

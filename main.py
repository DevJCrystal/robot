import os
import time
import logging
import threading

# Pi-Top
from pitop import Pitop
from pitop import UltrasonicSensor
from pitop import ServoMotor, ServoMotorSetting

# If window (nt) then cls else clear (mac / linux)
def clear():
    _ = os.system('cls' if os.name == 'nt' else 'clear')

class Robot:
    def __init__(self) -> None:

        self.clear_logs = True
        self.debug_mode_enabled = True

        # Battery
        self.battery = Pitop().battery

        # Distance in CM
        self.eyes_distance = 3
        self.update_eyes_loop = True
        self.eyes_sensor = UltrasonicSensor('D5')

        # Eyes Servo
        # Pos Angle = Left | Neg = Right
        self.eyes_servo = ServoMotor("S3")
        self.eyes_servo.target_angle = 0
        self.eyes_servo_current_angle = 0

    def update_eyes(self):
        while self.update_eyes_loop:

            self.eyes_distance = self.eyes_sensor.distance
            time.sleep(.25)

    def update_servo_angle(self, angle):
        self.eyes_servo.target_angle = angle
        self.eyes_servo_current_angle = angle

    def look_around(self):
        while self.update_eyes_loop:
            if self.eyes_distance <= 0.15:

                furthest_distance = 0
                furthest_distance_angle = 0

                # Look for a greater distance.
                for angle in range(90, -100, -30):
                    self.update_servo_angle(angle)
                    time.sleep(1)
                    if self.eyes_distance > furthest_distance:
                        furthest_distance = self.eyes_distance
                        furthest_distance_angle = angle

                print(f'Need to turn to this angle: {furthest_distance_angle}')
            else:
                if not self.eyes_servo_current_angle == 0:
                    self.update_servo_angle(0)

    def debug_mode(self):
        while self.debug_mode_enabled:

            if self.clear_logs:
                clear()

            print(f"Debug Log")
            
            if self.update_eyes_loop:
                logging.info(f"Battery Capacity: {self.battery.capacity}")
                logging.info(f"Battery is charging: {self.battery.is_charging}")
                logging.info(f"update_eyes_loop: {self.eyes_distance}")
                logging.info(f"eyes_servo_current_angle: {self.eyes_servo_current_angle}")

            time.sleep(.75)
            

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%I:%M:%S %p")
                    
    ptop = Robot()

    threading.Thread(target=ptop.debug_mode).start()
    threading.Thread(target=ptop.update_eyes).start()
    threading.Thread(target=ptop.look_around).start()
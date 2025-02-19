from PyQt5.QtCore import QThread, pyqtSignal
from pymavlink import mavutil
from baglanma import mavlink_connection
import time

class MAVLinkDataThread(QThread):
    ins_health_updated = pyqtSignal(bool)
    mag_health_updated = pyqtSignal(bool)
    ahrs_health_updated = pyqtSignal(bool)
    ekf_health_updated = pyqtSignal(bool)
    pre_health_updated = pyqtSignal(bool)
    temperature_updated = pyqtSignal(float)
    armed_status_updated = pyqtSignal(bool)
    altitude_updated = pyqtSignal(float)
    status_text_updated = pyqtSignal(str)
    pwm_updated = pyqtSignal(dict)
    gps_satellite_updated = pyqtSignal(int)
    vfr_hud_updated = pyqtSignal(int, float, float, float, float, int)
    throttle_updated = pyqtSignal(int)
    battery_updated = pyqtSignal(float, float, int)  # Voltaj, akım, kalan batarya

    def __init__(self):
        super().__init__()
        self._running = True
        self.mavlink_connection = mavlink_connection  # Tanımlama eklendi

    def run(self):
        while self._running:
            try:
                msg = self.mavlink_connection.recv_msg()
                if msg:
                    self.process_message(msg)
            except Exception as e:
                print(f"Error in MAVLinkDataThread: {e}")

            time.sleep(0.01)  # 10 ms bekle (gereksiz CPU yükünü önler)

    def process_message(self, msg):
        if msg.get_type() == "SYS_STATUS":
            ins_healthy = (
                bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_3D_ACCEL) and
                bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_3D_GYRO)
            )
            mag_healthy = bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_3D_MAG)
            ahrs_healthy = bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_ATTITUDE_STABILIZATION)
            ekf_healthy = bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_TERRAIN)
            pre_healthy = bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_ABSOLUTE_PRESSURE)

            self.ins_health_updated.emit(ins_healthy)
            self.mag_health_updated.emit(mag_healthy)
            self.ahrs_health_updated.emit(ahrs_healthy)
            self.ekf_health_updated.emit(ekf_healthy)
            self.pre_health_updated.emit(pre_healthy)

        elif msg.get_type() == "BATTERY_STATUS":
            voltage = msg.voltages[0] / 1000.0  # mV -> V
            current = msg.current_battery / 100.0  # cA -> A
            remaining = msg.battery_remaining  # Yüzde
            self.battery_updated.emit(voltage, current, remaining)

        elif msg.get_type() == "SCALED_PRESSURE":
            temperature = msg.temperature / 100.0  # Hatalı değişken düzeltildi
            self.temperature_updated.emit(temperature)

        elif msg.get_type() == "HEARTBEAT":
            armed = msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
            self.armed_status_updated.emit(bool(armed))

        elif msg.get_type() == "GLOBAL_POSITION_INT":
            altitude = msg.relative_alt / 1000.0
            self.altitude_updated.emit(altitude)

        elif msg.get_type() == "STATUSTEXT":
            self.status_text_updated.emit(msg.text)

        elif msg.get_type() == "SERVO_OUTPUT_RAW":
            pwm_data = {
                "servo1": msg.servo1_raw,
                "servo2": msg.servo2_raw,
                "servo3": msg.servo3_raw,
                "servo4": msg.servo4_raw,
            }
            self.pwm_updated.emit(pwm_data)

        elif msg.get_type() == "GPS_RAW_INT":
            self.gps_satellite_updated.emit(msg.satellites_visible)

        elif msg.get_type() == "VFR_HUD":
            heading = msg.heading
            airspeed = round(float(msg.airspeed), 2)
            groundspeed = round(float(msg.groundspeed), 2)
            altitude = round(float(msg.alt), 2)
            climb = round(float(msg.climb), 2)
            throttle = msg.throttle
            self.vfr_hud_updated.emit(heading, airspeed, groundspeed, altitude, climb, throttle)

        elif msg.get_type() == "RC_CHANNELS":
            throttle_pwm = msg.chan3_raw
            throttle_percent = int((throttle_pwm - 1000) / 10)
            throttle_percent = max(0, min(100, throttle_percent))
            self.throttle_updated.emit(throttle_percent)

    def stop(self):
        self._running = False
        self.quit()
        if not self.wait(3000):  # 3 saniye bekle
            self.terminate()  # Kapanmazsa zorla durdur
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
        """Tüm MAVLink verilerini tek thread içinde okur ve sinyallerle dağıtır."""
        while self._running:
            try:
                # SYS_STATUS mesajını oku (Sensör sağlık bilgileri buradan geliyor)
                msg = self.mavlink_connection.recv_match(type="SYS_STATUS", blocking=True, timeout=2)
                if msg and hasattr(msg, "onboard_control_sensors_health"):
                    ins_healthy = (
                        bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_3D_ACCEL) and
                        bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_3D_GYRO)
                    )
                    mag_healthy = bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_3D_MAG)
                    ahrs_healthy = bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_ATTITUDE_STABILIZATION)
                    ekf_healthy = bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_TERRAIN)
                    pre_healthy = bool(msg.onboard_control_sensors_health & mavutil.mavlink.MAV_SYS_STATUS_SENSOR_ABSOLUTE_PRESSURE)

                    # GUI'ye sinyalleri gönder
                    self.ins_health_updated.emit(ins_healthy)
                    self.mag_health_updated.emit(mag_healthy)
                    self.ahrs_health_updated.emit(ahrs_healthy)
                    self.ekf_health_updated.emit(ekf_healthy)
                    self.pre_health_updated.emit(pre_healthy)

                # BATTERY_STATUS mesajını oku
                msg_battery = self.mavlink_connection.recv_match(type="BATTERY_STATUS", blocking=True, timeout=2)
                if msg_battery:
                    voltage = msg_battery.voltages[0] / 1000.0  # mV -> V
                    current = msg_battery.current_battery / 100.0  # cA -> A
                    remaining = msg_battery.battery_remaining  # Yüzde

                    self.battery_updated.emit(voltage, current, remaining)


                # SCALED_PRESSURE mesajından sıcaklık al
                msg_tempature = self.mavlink_connection.recv_match(type="SCALED_PRESSURE", blocking=True, timeout=2)
                if msg_tempature:
                    temperature = msg_tempature.temperature / 100.0  # Hatalı değişken düzeltildi
                    self.temperature_updated.emit(temperature)

                msg_arm = self.mavlink_connection.recv_match(type="HEARTBEAT", blocking=True, timeout=1)
                if msg_arm:
                    armed = msg_arm.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
                    self.armed_status_updated.emit(bool(armed))

                msg_altitude = self.mavlink_connection.recv_match(type="GLOBAL_POSITION_INT", blocking=True,timeout=1)
                if msg_altitude:
                    altitude = msg_altitude.relative_alt / 1000.0
                    self.altitude_updated.emit(altitude)

                msg_status_text = self.mavlink_connection.recv_match(type="STATUSTEXT", blocking=True,timeout=1)
                if msg_status_text:
                    self.status_text_updated.emit(msg_status_text.text)

                msg_servo_output = self.mavlink_connection.recv_match(type="SERVO_OUTPUT_RAW", blocking=True, timeout=1)
                if msg_servo_output:
                    pwm_data = {
                        "servo1": msg_servo_output.servo1_raw,
                        "servo2": msg_servo_output.servo2_raw,
                        "servo3": msg_servo_output.servo3_raw,
                        "servo4": msg_servo_output.servo4_raw,
                    }
                    self.pwm_updated.emit(pwm_data)

                msg_gps_count = self.mavlink_connection.recv_match(type="GPS_RAW_INT", blocking=True, timeout=1)
                if msg_gps_count:
                    self.gps_satellite_updated.emit(msg_gps_count.satellites_visible)

                msg_vfr = mavlink_connection.recv_match(type="VFR_HUD", blocking=True, timeout=2)
                if msg_vfr:
                    heading = msg_vfr.heading
                    airspeed = round(float(msg_vfr.airspeed), 2)
                    groundspeed = round(float(msg_vfr.groundspeed), 2)
                    altitude = round(float(msg_vfr.alt), 2)
                    climb = round(float(msg_vfr.climb), 2)
                    throttle = msg_vfr.throttle

                    self.vfr_hud_updated.emit(heading, airspeed, groundspeed, altitude, climb, throttle)

                msg_throttle = mavlink_connection.recv_match(type="RC_CHANNELS", blocking=True, timeout=1)
                if msg_throttle:
                    throttle_pwm = msg_throttle.chan3_raw
                    throttle_percent = int((throttle_pwm - 1000) / 10)
                    throttle_percent = max(0, min(100, throttle_percent))
                    self.throttle_updated.emit(throttle_percent)


            except Exception as e:
                print(f"Error in MAVLinkDataThread: {e}")

            time.sleep(1)  # 1 saniye bekle (gereksiz CPU yükünü önler)

    def stop(self):
        """Thread'i güvenli şekilde durdurur."""
        self._running = False
        self.quit()
        if not self.wait(3000):  # 3 saniye bekle
            self.terminate()  # Kapanmazsa zorla durdur



class MAVLinkThrottleThread(QThread):
    throttle_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._running = True

    def run(self):
        while self._running:
            try:
                msg = mavlink_connection.recv_match(type="RC_CHANNELS", blocking=True, timeout=1)
                if msg is None:
                    print("No valid RC_CHANNELS message received.")
                    continue  # Eğer mesaj gelmediyse döngüye devam et

                if hasattr(msg, "chan3_raw"):
                    throttle_pwm = msg.chan3_raw
                    throttle_percent = int((throttle_pwm - 1000) / 10)
                    throttle_percent = max(0, min(100, throttle_percent))
                    self.throttle_updated.emit(throttle_percent)
                else:
                    print("RC_CHANNELS message received but missing chan3_raw attribute.")
            except:
                pass

    def stop(self):
        self._running = False
        self.quit()
        self.wait()
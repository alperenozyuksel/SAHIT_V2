import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QProgressBar, \
    QTextEdit
from PyQt5.QtGui import QPalette, QColor, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt, QTimer
import altitude_inducator
import yellow_arrow
from sensorler import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()



        self.setWindowTitle("ŞAHİT")
        self.setGeometry(100, 100, 1920, 1080)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("black"))
        self.setPalette(palette)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(self.create_tab("Sekme 1"), "Sekme 1")
        self.tabs.addTab(self.create_sekme_2(), "Sekme 2")
        self.tabs.addTab(self.create_tab("Sekme 3"), "Sekme 3")



        self.mavlink_thread = MAVLinkDataThread()
        self.mavlink_thread.ins_health_updated.connect(self.updated_ins)
        self.mavlink_thread.mag_health_updated.connect(self.updated_mag)
        self.mavlink_thread.ahrs_health_updated.connect(self.updated_ahrs)
        self.mavlink_thread.ekf_health_updated.connect(self.updated_ekf)
        self.mavlink_thread.pre_health_updated.connect(self.updated_pre)
        self.mavlink_thread.battery_updated.connect(self.updated_battery)
        self.mavlink_thread.temperature_updated.connect(self.update_temperature)
        self.mavlink_thread.armed_status_updated.connect(self.update_arm)
        self.mavlink_thread.altitude_updated.connect(self.update_altitude)
        self.mavlink_thread.status_text_updated.connect(self.add_status_message)
        self.mavlink_thread.pwm_updated.connect(self.update_progress_bars)
        self.mavlink_thread.gps_satellite_updated.connect(self.updated_gps_count)
        self.mavlink_thread.vfr_hud_updated.connect(self.updated_vfr)
        self.mavlink_thread.throttle_updated.connect(self.update_throttle)
        self.mavlink_thread.start()





        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all)  # Her zamanlayıcıda yeniden çiz
        self.timer.start(100)  # Her 100ms'de bir

    def create_tab(self, title):
        tab = QWidget()
        tab_layout = QVBoxLayout()
        label = QLabel(title)
        label.setStyleSheet("color: white; font-size: 24px;")
        tab_layout.addWidget(label)
        tab.setLayout(tab_layout)
        tab.setStyleSheet("background-color: #000000;")
        return tab

    def create_sekme_2(self):
        tab = QWidget()



        self.image_label = QLabel(tab)
        pixmap = QPixmap("images/droneimg.png")
        scaled_pixmap = pixmap.scaled(1000, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.move(480, 200)

        self.logo = QLabel(tab)
        pixmap_2 = QPixmap("images/SONYAKAMOZ1.png")
        scaled_pixmap_2 = pixmap_2.scaled(300, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(scaled_pixmap_2)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.move(500,800)


        self.resim_yolu = "batarya/1.png"
        self.ibre_batarya_100 = QLabel(tab)
        self.pixmap_7 = QPixmap(self.resim_yolu)
        scaled_pixmap_7 = self.pixmap_7.scaled(180, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.ibre_batarya_100.setPixmap(scaled_pixmap_7)
        self.ibre_batarya_100.setAlignment(Qt.AlignCenter)
        self.ibre_batarya_100.setStyleSheet("background: transparent;")
        self.ibre_batarya_100.move(885, 340)

        self.ibre_devir = QLabel(tab)
        pixmap_1 = QPixmap("images/ibre2.png")
        scaled_pixmap_1 = pixmap_1.scaled(200, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ibre_devir.setPixmap(scaled_pixmap_1)
        self.ibre_devir.setAlignment(Qt.AlignCenter)
        self.ibre_devir.move(80, 20)

        self.ibre_heading = QLabel(tab)
        pixmap_3 = QPixmap("images/ibre5.png")
        scaled_pixmap_3 = pixmap_3.scaled(200, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ibre_heading.setPixmap(scaled_pixmap_3)
        self.ibre_heading.setAlignment(Qt.AlignCenter)
        self.ibre_heading.move(390, 20)

        self.ibre_air_speed = QLabel(tab)
        pixmap_4 = QPixmap("images/ibre7.png")
        scaled_pixmap_4 = pixmap_4.scaled(200, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ibre_air_speed.setPixmap(scaled_pixmap_4)
        self.ibre_air_speed.setAlignment(Qt.AlignCenter)
        self.ibre_air_speed.move(700, 20)


        self.ibre_gps_speed = QLabel(tab)
        pixmap_6 = QPixmap("images/ibre7.png")
        scaled_pixmap_6 = pixmap_6.scaled(200, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ibre_gps_speed.setPixmap(scaled_pixmap_6)
        self.ibre_gps_speed.setAlignment(Qt.AlignCenter)
        self.ibre_gps_speed.move(1055, 20)

        self.ibre_dikilme = QLabel(tab)
        pixmap_5 = QPixmap("images/ibre3.png")
        scaled_pixmap_5 = pixmap_5.scaled(200, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ibre_dikilme.setPixmap(scaled_pixmap_5)
        self.ibre_dikilme.setAlignment(Qt.AlignCenter)
        self.ibre_dikilme.move(1365, 20)

        self.ibre_gyroscope = QLabel(tab)
        pixmap_9 = QPixmap("images/ibre5.png")
        scaled_pixmap_9 = pixmap_9.scaled(200, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ibre_gyroscope.setPixmap(scaled_pixmap_9)
        self.ibre_gyroscope.setAlignment(Qt.AlignCenter)
        self.ibre_gyroscope.move(1645, 20)


        self.ibre_voltaj = QLabel(tab)
        pixmap_5 = QPixmap("images/deneme.png")
        scaled_pixmap_5 = pixmap_5.scaled(175, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ibre_voltaj.setPixmap(scaled_pixmap_5)
        self.ibre_voltaj.setAlignment(Qt.AlignCenter)
        self.ibre_voltaj.setStyleSheet("background: transparent;")
        self.ibre_voltaj.move(680, 400)

        self.ibre_amper = QLabel(tab)
        pixmap_8 = QPixmap("images/ibre10.png")
        scaled_pixmap_8 = pixmap_8.scaled(175, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ibre_amper.setPixmap(scaled_pixmap_8)
        self.ibre_amper.setAlignment(Qt.AlignCenter)
        self.ibre_amper.setStyleSheet("background: transparent;")
        self.ibre_amper.move(1080, 400)




        self.imu_labels = ["GPS","INS","MAG","AHRS","EKF","PRE","SICAKLIK"]
        self.imu_frames = []
        for i in range(7):
            box = QFrame(tab)
            box.setFrameShape(QFrame.Box)
            box.setStyleSheet("background-color: #000000; border: 1px solid white;")
            box.setFixedSize(100, 25)
            box.move(1200, 790 + i * 30)

            label = QLabel(self.imu_labels[i], box)
            label.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
            label.setAlignment(Qt.AlignCenter)
            self.imu_frames.append(box)



        self.motor_labels = ["MOTOR 1","MOTOR 2"]
        self.motor_frames = []

        for i in range(2):
            box = QFrame(tab)
            box.setFrameShape(QFrame.Box)
            box.setStyleSheet("background-color: #000000; border: 2px solid white;")
            box.setFixedSize(100, 25)
            box.move(850, 290 + i * 350)

            label = QLabel(self.motor_labels[i], box)
            label.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
            label.setAlignment(Qt.AlignCenter)
            self.motor_frames.append(box)

        self.motor_labels_2 = ["MOTOR 3","MOTOR 4"]
        self.motor_frames_2 = []
        for i in range(2):
            box = QFrame(tab)
            box.setFrameShape(QFrame.Box)
            box.setStyleSheet("background-color: #000000; border: 2px solid white;")
            box.setFixedSize(100, 25)
            box.move(1005, 290 + i * 350)

            label = QLabel(self.motor_labels_2[i], box)
            label.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
            label.setAlignment(Qt.AlignCenter)
            self.motor_frames_2.append(box)




        self.motor_bars = []
        for i in range(4):
            box = QFrame(tab)
            box.setFrameShape(QFrame.Box)
            box.setStyleSheet("background-color: #444444; border: 2px solid white;")
            box.setFixedSize(50, 200)
            box.move(870 + i * 59, 800)

            label = QLabel(f"Motor {i+1}", tab)
            label.setStyleSheet("color: white; font-weight: bold; font-size: 12px")
            label.move(873 + i * 59, 770)

            bar = QProgressBar(box)
            bar.setGeometry(5, 5, 40, 190)
            bar.setStyleSheet("QProgressBar { background-color: #222222; border: none; } "
                              "QProgressBar::chunk { background-color: #00FF00; }")
            bar.setOrientation(Qt.Vertical)
            bar.setMaximum(2000)
            bar.setMinimum(1000)

            self.motor_bars.append(bar)



        self.sicaklik_frame = QFrame(tab)
        self.sicaklik_frame.setFrameShape(QFrame.Box)
        self.sicaklik_frame.setStyleSheet("background-color: #000000; border: 2px solid green;")
        self.sicaklik_frame.setFixedSize(100, 25)
        self.sicaklik_frame.move(1815, 950)

        self.pusula_frame = QFrame(tab)
        self.pusula_frame.setFrameShape(QFrame.Box)
        self.pusula_frame.setStyleSheet("background-color: #000000; border: 2px solid green;")
        self.pusula_frame.setFixedSize(100, 25)
        self.pusula_frame.move(1815, 970)


        self.label_sicaklik = QLabel("SICAKLIK", self.sicaklik_frame)
        self.label_sicaklik.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        self.label_sicaklik.setAlignment(Qt.AlignCenter)

        label_sicaklik_yazi = QLabel("FCC Sıcaklık", tab)
        label_sicaklik_yazi.setStyleSheet("color: white; font-weight: bold;")
        label_sicaklik_yazi.move(1727, 953)

        label_gaz_yazi = QLabel("GAZ", tab)
        label_gaz_yazi.setStyleSheet("color: white; font-weight: bold;")
        label_gaz_yazi.move(1300, 300)

        label_devir_yazi = QLabel("DEVİR", tab)
        label_devir_yazi.setStyleSheet("color: white; font-weight: bold;")
        label_devir_yazi.move(158, 220)

        label_heading_yazi = QLabel("HEADING", tab)
        label_heading_yazi.setStyleSheet("color: white; font-weight: bold;")
        label_heading_yazi.move(453, 220)

        label_airspeed_yazi = QLabel("AIRSPEED", tab)
        label_airspeed_yazi.setStyleSheet("color: white; font-weight: bold;")
        label_airspeed_yazi.move(763, 220)

        label_gpspeed_yazi = QLabel("GPSSPEED", tab)
        label_gpspeed_yazi.setStyleSheet("color: white; font-weight: bold;")
        label_gpspeed_yazi.move(1118, 220)

        label_dikilme_yazi = QLabel("DİKİLME", tab)
        label_dikilme_yazi.setStyleSheet("color: white; font-weight: bold;")
        label_dikilme_yazi.move(1433, 220)

        label_horizon_yazi = QLabel("HORIZON", tab)
        label_horizon_yazi.setStyleSheet("color: white; font-weight: bold;")
        label_horizon_yazi.move(1710, 220)

        self.dis_sicaklik_frame = QFrame(tab)
        self.dis_sicaklik_frame.setFrameShape(QFrame.Box)
        self.dis_sicaklik_frame.setStyleSheet("background-color: #000000; border: 2px solid green;")
        self.dis_sicaklik_frame.setFixedSize(100, 25)
        self.dis_sicaklik_frame.move(1815, 970)

        self.label_dis_sicaklik = QLabel(f"{35:.2f}°C", self.dis_sicaklik_frame)
        self.label_dis_sicaklik.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        self.label_dis_sicaklik.setAlignment(Qt.AlignCenter)

        label_dis_sicaklik_yazi = QLabel("Dış Sıcaklık", tab)
        label_dis_sicaklik_yazi.setStyleSheet("color: white; font-weight: bold;")
        label_dis_sicaklik_yazi.move(1730, 974)

        self.global_altitude = altitude_inducator.ScaleWidget(tab)
        self.global_altitude.setGeometry(600, 200, 50, 600)

        self.relative_altitude = altitude_inducator.ScaleWidget(tab)
        self.relative_altitude.setGeometry(400, 252, 50, 550)

        self.throttle = altitude_inducator.ScaleWidget(tab)
        self.throttle.setGeometry(1300, 300, 50, 400)

        self.sistem_zamani = QFrame(tab)
        self.sistem_zamani.setFrameShape(QFrame.Box)
        self.sistem_zamani.setStyleSheet("background-color: #000000; border: 1px solid white;")
        self.sistem_zamani.setFixedSize(125, 25)
        self.sistem_zamani.move(1810, 10)

        self.batarya_kalan = QFrame(tab)
        self.batarya_kalan.setFrameShape(QFrame.Box)
        self.batarya_kalan.setStyleSheet("background-color: #000000; border: 0px solid green;")
        self.batarya_kalan.setFixedSize(50, 25)
        self.batarya_kalan.move(952, 465)

        self.label_batarya = QLabel("BATARYA", self.batarya_kalan)
        self.label_batarya.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        self.label_batarya.setAlignment(Qt.AlignCenter)


        for i in range(0, 301, 25):
            label = QLabel(str(i), tab)
            label.setStyleSheet("color: white; font-weight: bold; font-size: 10px")
            label.move(580, int(772 - (i * 1.854)))
        for i in range(0, 301, 25):
            label = QLabel(str(i), tab)
            label.setStyleSheet("color: white; font-weight: bold; font-size: 10px")
            label.move(380, 772 - int((i * 1.68)))

        for i in range(0, 101, 10):
            label = QLabel(str(i), tab)
            label.setStyleSheet("color: white; font-weight: bold; font-size: 10px")
            label.move(1270, 670 - int((i * 3.5)))

        self.yukselik_etiketi = QFrame(tab)
        self.yukselik_etiketi.setFrameShape(QFrame.Box)
        self.yukselik_etiketi.setStyleSheet("background-color: #000000; border: 2px solid white;")
        self.yukselik_etiketi.setFixedSize(50, 20)
        self.yukselik_etiketi.move(640, 772)

        self.label_yukseklik_etiketi = QLabel("YUKSEKLIK", self.yukselik_etiketi)
        self.label_yukseklik_etiketi.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        self.label_yukseklik_etiketi.setAlignment(Qt.AlignCenter)





        self.yellow_arrow = yellow_arrow.YellowArrow(tab)
        self.yellow_arrow.setGeometry(100, 100, 100, 100)  # Adjust position and size as needed
        self.yellow_arrow.set_angle(270)
        self.yellow_arrow.move(605,500)

        self.yellow_arrow_2 = yellow_arrow.YellowArrow(tab)
        self.yellow_arrow_2.setGeometry(100, 100, 100, 100)  # Adjust position and size as needed
        self.yellow_arrow_2.set_angle(270)
        self.yellow_arrow_2.move(405, 500)

        self.yellow_arrow_throttle = yellow_arrow.YellowArrow(tab)
        self.yellow_arrow_throttle.setGeometry(100, 100, 100, 100)  # Adjust position and size as needed
        self.yellow_arrow_throttle.set_angle(270)
        self.yellow_arrow_throttle.move(1302, 630)

        self.yukselik_etiketi_sea = QFrame(tab)
        self.yukselik_etiketi_sea.setFrameShape(QFrame.Box)
        self.yukselik_etiketi_sea.setStyleSheet("background-color: #000000; border: 2px solid white;")
        self.yukselik_etiketi_sea.setFixedSize(50, 20)
        self.yukselik_etiketi_sea.move(460, 772)

        self.label_yukseklik_etiketi_sea = QLabel("YUKSEKLIK", self.yukselik_etiketi_sea)
        self.label_yukseklik_etiketi_sea.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        self.label_yukseklik_etiketi_sea.setAlignment(Qt.AlignCenter)

        self.label_sistem_zamani = QLabel("ZAMAN", self.sistem_zamani)
        self.label_sistem_zamani.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        self.label_sistem_zamani.setAlignment(Qt.AlignCenter)

        self.heading_frame = QFrame(tab)
        self.heading_frame.setFrameShape(QFrame.Box)
        self.heading_frame.setStyleSheet("background-color: #000000; border: 2px solid white;")
        self.heading_frame.setFixedSize(50, 20)
        self.heading_frame.move(550, 20)

        self.label_heading = QLabel("HEADING", self.heading_frame)
        self.label_heading.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        self.label_heading.setAlignment(Qt.AlignCenter)

        self.airspeed_frame = QFrame(tab)
        self.airspeed_frame.setFrameShape(QFrame.Box)
        self.airspeed_frame.setStyleSheet("background-color: #000000; border: 2px solid white;")
        self.airspeed_frame.setFixedSize(50, 20)
        self.airspeed_frame.move(854, 20)

        self.label_airspeed = QLabel("AIRSPEED", self.airspeed_frame)
        self.label_airspeed.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        self.label_airspeed.setAlignment(Qt.AlignCenter)

        self.gpsspeed_frame = QFrame(tab)
        self.gpsspeed_frame.setFrameShape(QFrame.Box)
        self.gpsspeed_frame.setStyleSheet("background-color: #000000; border: 2px solid white;")
        self.gpsspeed_frame.setFixedSize(50, 20)
        self.gpsspeed_frame.move(1210, 20)

        self.label_gpsspeed = QLabel("GPSPEED", self.gpsspeed_frame)
        self.label_gpsspeed.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        self.label_gpsspeed.setAlignment(Qt.AlignCenter)

        self.label_voltaj_text = QLabel("VOLTAJ", tab)
        self.label_voltaj_text.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        self.label_voltaj_text.setAlignment(Qt.AlignCenter)
        self.label_voltaj_text.move(743,530)

        self.label_amper_text = QLabel("AMPER", tab)
        self.label_amper_text.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        self.label_amper_text.setAlignment(Qt.AlignRight)
        self.label_amper_text.move(1145, 530)

        self.label_batarya_text = QLabel("BATARYA", tab)
        self.label_batarya_text.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        self.label_batarya_text.setAlignment(Qt.AlignCenter)
        self.label_batarya_text.move(950, 500)

        self.status_text_box = QTextEdit(tab)
        self.status_text_box.setReadOnly(True)
        self.status_text_box.setStyleSheet("background-color: gray; color: white; font-size: 12px;")
        self.status_text_box.setGeometry(1340, 845, 300, 150)  # (x, y, width, height)

        self.ibre = QLabel(tab)
        self.pixmap_10 = QPixmap("images/ok.png")
        # 90 derece döndürme
        transform = QTransform().rotate(90)
        rotated_pixmap = self.pixmap_10.transformed(transform, Qt.SmoothTransformation)
        self.scaled_pixmap = rotated_pixmap.scaled(100, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # Döndürülmüş resmi QLabel'e ekleme
        self.ibre.setPixmap(self.scaled_pixmap)
        self.ibre.setAlignment(Qt.AlignCenter)
        self.ibre.setStyleSheet("background: transparent;")
        self.ibre.move(799, 50)
        self.pivot_point = self.scaled_pixmap.rect().center()  # Resmin merkezi
        self.pivot_point.setY(self.scaled_pixmap.height())

        self.voltaj_frame = QFrame(tab)
        self.voltaj_frame.setFrameShape(QFrame.Box)
        self.voltaj_frame.setStyleSheet("background-color: #000000; border: 2px solid white;")
        self.voltaj_frame.setFixedSize(50, 20)
        self.voltaj_frame.move(741, 550)

        self.label_voltaj = QLabel("VOLTAJ", self.voltaj_frame)
        self.label_voltaj.setAlignment(Qt.AlignCenter)
        self.label_voltaj.setStyleSheet("color: white; font-size: 12px;")

        self.amper_frame = QFrame(tab)
        self.amper_frame.setFrameShape(QFrame.Box)
        self.amper_frame.setStyleSheet("background-color: #000000; border: 1px solid white;")
        self.amper_frame.setFixedSize(50, 20)
        self.amper_frame.move(1142, 550)

        self.label_amper = QLabel("AMPER", tab)
        self.label_amper.setStyleSheet("color: white; font-size: 11px; border: 0px")
        self.label_amper.setAlignment(Qt.AlignCenter)
        self.label_amper.move(1151, 554)


        tab.setStyleSheet("background-color: #000000;")




        return tab

    def update_progress_bars(self, data):
        for i, bar in enumerate(self.motor_bars):
            bar.setValue(data[f"servo{i+1}"])



    def update_temperature(self, temperature):
        self.label_sicaklik.setText(f"{temperature:.2f}°C")
        if 30 < temperature < 40:
            self.label_sicaklik.setStyleSheet("background-color: #00FF00;")
            self.imu_frames[6].setStyleSheet("background-color: #00FF00; border: 2px solid white;")
        elif temperature < 30:
            self.label_sicaklik.setStyleSheet("background-color: #FF0000;")
            self.imu_frames[6].setStyleSheet("background-color: #FF0000; border: 2px solid white;")

    def update_altitude(self, relative_alt):
        global_yukseklik = int(relative_alt)
        self.label_yukseklik_etiketi.setText(f"{global_yukseklik}")
        yeni_y = 772 - (global_yukseklik * 1.9)
        yeni_y = max(50, min(yeni_y, 772))
        self.yukselik_etiketi.move(660, int(yeni_y))
        self.yellow_arrow.move(605, int(yeni_y - 40))

    def update_throttle(self, chan3_raw):
        throttle = int(chan3_raw)
        yeni_y = 630 - (throttle * 3.58)
        yeni_y = max(50, min(yeni_y, 630))
        self.yellow_arrow_throttle.move(1302, int(yeni_y))

    def update_arm(self, base_mode):

        if base_mode == True:
            self.motor_frames[0].setStyleSheet("background-color: #00FF00; border: 2px solid white;")
            self.motor_frames[1].setStyleSheet("background-color: #00FF00; border: 2px solid white;")
            self.motor_frames_2[0].setStyleSheet("background-color: #00FF00; border: 2px solid white;")
            self.motor_frames_2[1].setStyleSheet("background-color: #00FF00; border: 2px solid white;")
        elif base_mode == False:
            self.motor_frames[0].setStyleSheet("background-color: #FF0000; border: 2px solid white;")
            self.motor_frames[1].setStyleSheet("background-color: #FF0000; border: 2px solid white;")
            self.motor_frames_2[0].setStyleSheet("background-color: #FF0000; border: 2px solid white;")
            self.motor_frames_2[1].setStyleSheet("background-color: #FF0000; border: 2px solid white;")

    def updated_ins(self, ins_healthy):

        if ins_healthy == True:
            self.imu_frames[1].setStyleSheet("background-color: #00FF00; border: 1px solid white;")

        elif ins_healthy == False:
            self.imu_frames[1].setStyleSheet("background-color: #FF0000; border: 1px solid white;")


    def updated_mag(self, mag_healthy):

        if mag_healthy == True:
            self.imu_frames[2].setStyleSheet("background-color: #00FF00; border: 1px solid white;")

        elif mag_healthy == False:
            self.imu_frames[2].setStyleSheet("background-color: #FF0000; border: 1px solid white;")


    def updated_ahrs(self, ahrs_healthy):
        if ahrs_healthy == True:
            self.imu_frames[3].setStyleSheet("background-color: #00FF00; border: 1px solid white;")

        elif ahrs_healthy == False:
            self.imu_frames[3].setStyleSheet("background-color: #FF0000; border: 1px solid white;")


    def updated_ekf(self, ekf_healthy):
        if ekf_healthy == True:
            self.imu_frames[4].setStyleSheet("background-color: #00FF00; border: 1px solid white;")

        elif ekf_healthy == False:
            self.imu_frames[4].setStyleSheet("background-color: #FF0000; border: 1px solid white;")


    def updated_pre(self, pre_healthy):
        if pre_healthy == True:
            self.imu_frames[5].setStyleSheet("background-color: #00FF00; border: 1px solid white;")

        elif pre_healthy == False:
            self.imu_frames[5].setStyleSheet("background-color: #FF0000; border: 1px solid white;")

    def updated_system_time(self, time_unix_usec, time_boot_ms):
        self.label_sistem_zamani.setText(f"{time_unix_usec}, {time_boot_ms}")

    def add_status_message(self, message):
        """STATUSTEXT mesajlarını ekler ve en son mesaja kaydırır"""
        self.status_text_box.append(message)

        # Otomatik olarak en son mesaja kaydır
        scrollbar = self.status_text_box.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def updated_gps_count(self, satellite_count):
        if satellite_count > 9:
            self.imu_frames[0].setStyleSheet("background-color: #00FF00; border: 1px solid white;")
        elif satellite_count < 10:
            self.imu_frames[0].setStyleSheet("background-color: #FF0000; border: 1px solid white;")


    def updated_battery(self, voltage,current,remaining):

        self.label_batarya.setText(f"%{remaining}")
        self.label_voltaj.setText(f"{voltage}")
        self.label_amper.setText(f"{current}")


        image_index = 15 - int((remaining / 100.0) * 15)
        image_index = max(1, min(image_index, 15))  # 1 ile 15 arasında sınırla

        self.resim_yolu = f"batarya/{image_index}.png"

        self.update_battery_image()

    def update_battery_image(self):
        new_pixmap = QPixmap(self.resim_yolu)
        scaled_pixmap = new_pixmap.scaled(180, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.ibre_batarya_100.setPixmap(scaled_pixmap)

    def updated_vfr(self,heading, airspeed, groundspeed, altitude, climb, throttle):

        self.label_heading.setText(f"{heading}")
        self.label_airspeed.setText(f"{airspeed}")
        self.label_gpsspeed.setText(f"{groundspeed}")
        self.angle = airspeed * 1.8  # 0-100 hız için 0-180 derece
        self.update_needle_angle(self.angle)

    def update_needle_angle(self, angle):
        # İbrenin açısını güncelleme
        transform = QTransform()
        # Dönüş merkezini (pivot noktasını) ibrenin en altına ayarla
        transform.translate(self.pivot_point.x(), self.pivot_point.y())
        transform.rotate(angle)
        transform.translate(-self.pivot_point.x(), -self.pivot_point.y())

        # Döndürülmüş resmi oluştur
        rotated_pixmap = self.scaled_pixmap.transformed(transform, Qt.SmoothTransformation)
        self.ibre.setPixmap(rotated_pixmap)

    def update_all(self):
        self.update()








if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
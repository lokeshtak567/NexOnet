from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, 
    QMainWindow, QFrame, QSystemTrayIcon, QMenu, 
)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction
from PyQt6.QtCore import (
    QTimer, QSettings, QThread, pyqtSignal, QPropertyAnimation, QPoint, 
    QEasingCurve, Qt
)
import sys
import os
import subprocess
from requests import session
import random
import ctypes

# --------- CONFIG ---------
idpool = [
    "R30000", "R30001", "R30005", "R30006", "R30007", 
    "R30011", "R30012", "R32560", "R32530", "R32510",
    "R30012", "R30013", "R30015", "R30016", "R30018", 
    "R30025", "R30027", "R30028", "R30031", "R30032",
    "R30033", "R30035", "R30036", "R30037", "R30038",

    "R42579", "R42575", "R43000", "R42789", "R43217",
    "R42702", "R42895", "R42727", "R43838", "R44076",
    "R40022", "R40023", "R44101", "R44102", "R43146",
    "R43147", "R43126", "R42976", "R43840", "R43844",
    "R43847", "R43850", "R43857", "R43859", "R43860", 
    "R43863", "R43864", "R43868", "R43859", "R43860",
]

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_cmd_silently(command, shell=False):
    """
    Run shell/CLI commands without opening a terminal window and capture output.
    Returns: (stdout, stderr, returncode)
    """
    kwargs = {
        "capture_output": True,
        "text": True,
    }
    if sys.platform.startswith("win"):
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    try:
        result = subprocess.run(command, shell=shell, **kwargs)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return '', str(e), 1

class ToggleSwitch(QFrame):
    toggled = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self.setStyleSheet("background-color: #3c3c3c; border-radius: 15px;")
        self.knob = QLabel(self)
        self.knob.setGeometry(3, 3, 24, 24)
        self.knob.setStyleSheet("""
            background-color: white;
            border-radius: 12px;
            margin: 0px;
        """)
        self.checked = False
        self.animation = QPropertyAnimation(self.knob, b"pos")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def mouseReleaseEvent(self, event):
        self.toggle()

    def toggle(self):
        if not self.checked:
            self.animation.setStartValue(QPoint(3, 3))
            self.animation.setEndValue(QPoint(33, 3))
            self.setStyleSheet("background-color: #00c896; border-radius: 15px;")
        else:
            self.animation.setStartValue(QPoint(33, 3))
            self.animation.setEndValue(QPoint(3, 3))
            self.setStyleSheet("background-color: #3c3c3c; border-radius: 15px;")
        self.animation.start()
        self.checked = not self.checked
        self.toggled.emit(self.checked)

    def setChecked(self, checked: bool):
        if self.checked == checked:
            return
        self.checked = checked
        if self.checked:
            self.knob.move(33, 3)
            self.setStyleSheet("background-color: #00c896; border-radius: 15px;")
        else:
            self.knob.move(3, 3)
            self.setStyleSheet("background-color: #3c3c3c; border-radius: 15px;")

    def isChecked(self):
        return self.checked

class WorkerThread(QThread):
    progress = pyqtSignal(str, str)
    def __init__(self):
        super().__init__()
        self._running = True
        self.user = None
        self.session = session()

    def run(self):
        while self._running:
            if self.check_captive_portal():
                self.progress.emit("animation_status", "Portal Found, Logging In...")
                self.progress.emit("wifi_status", "Connected ✅")
                if self.do_login_process():
                    self.check_internet()
                else:
                    continue
            else:
                continue
            QThread.msleep(400)

    def stop(self):
        if self.user:
            self.do_logout_process(self.user)
        self._running = False
        self.wait()

    def check_captive_portal(self):
        while self._running:
            try:
                resp = self.session.get("http://172.16.35.1:8090", timeout=3)
                return resp.status_code == 200
            except Exception:
                self.progress.emit("animation_status", "Connect to College WiFi ❗")
                QThread.msleep(2000)
                return False

    def do_login_process(self):
        LOGIN_URL = "http://172.16.35.1:8090/login.xml"
        for _ in range(3):
            if not self._running:
                break
            self.user = random.choice(idpool)
            login_payload = {
                "mode": "191",
                "username": self.user,
                "password": self.user,
                "a": "1743598790580",
                "producttype": "0",
            }
            try:
                resp = self.session.post(LOGIN_URL, data=login_payload, timeout=3)
                if resp.status_code == 200 and "signed in" in resp.text:
                    self.progress.emit("animation_status", f"{self.user} Logged In, checking internet...")
                    self.progress.emit("user_status", f"{self.user}")
                    return True
            except Exception as e:
                self.progress.emit("animation_status", f"{e}")
        return False

    def check_internet(self):
        while self._running:
            out, err, code = run_cmd_silently(['ping', '-n', '1', 'google.com'])
            if code == 0:
                self.progress.emit("internet_status", "connected ✅")
                self.progress.emit("animation_status", "Enjoy ✅")
                QThread.msleep(2000)
                continue
            else:
                emsg = f"Reconnecting ({err.strip()})" if err else "Reconnecting..."
                self.progress.emit("internet_status", "Disconnected ❌")
                self.progress.emit("animation_status", emsg)
                return False

    def do_logout_process(self, user):
        LOGOUT_URL = "http://172.16.35.1:8090/logout.xml"
        if not user:
            return
        logout_payload = {
            "mode": "193",
            "username": user,
            "a": "1743598790580",
            "producttype": "0"
        }
        for _ in range(3):
            try:
                resp = self.session.post(LOGOUT_URL, data=logout_payload, timeout=3)
                if resp.status_code == 200 and "signed out" in resp.text:
                    self.progress.emit("internet_status", "Disconnected ❌")
                    self.progress.emit("user_status", "None")
                    break
            except Exception as e:
                self.progress.emit("animation_status", f"{e}")

class NexOnetGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(self.resource_path("logo.ico")))
        self.setWindowTitle("NexOnet v1.1")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")
        self.settings = QSettings("NexOnetCompany", "NexOnetApp")
        self.worker_thread = None
        self.tray_icon = None
        self.init_ui()
        self.restore_toggle_states()
        self.init_tray()

    def resource_path(self, relative_path):
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # --- Logo Layout
        logo_layout = QVBoxLayout()
        logo_image = QLabel()
        logo_path = self.resource_path("logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(60,60, Qt.AspectRatioMode.KeepAspectRatio)
            logo_image.setPixmap(pixmap)
        else:
            logo_image.setText("[Logo]")
            logo_image.setStyleSheet("color: gray;")
        logo_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label = QLabel("NexOnet")
        logo_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("color: #00ffcc;")
        logo_layout.addWidget(logo_image)
        logo_layout.addWidget(logo_label)
        layout.addLayout(logo_layout)
        
        # --- Status ---
        self.status_box = QFrame()
        self.status_box.setStyleSheet("background-color: #2b2b3d; border-radius: 12px; padding: 8px;")
        status_layout = QVBoxLayout()
        self.wifi_status = QLabel("WiFi Status: Disconnected ❌")
        self.internet_status = QLabel("Internet: Disconnected ❌")
        self.user_status = QLabel("User: None")
        self.signal_status = QLabel("Signal Strength: ❗")
        self.animation_status = QLabel("")
        self.animation_status.setStyleSheet("color: #00ffcc")
        for label in [
            self.wifi_status,
            self.internet_status,
            self.user_status,
            self.signal_status,
            self.animation_status
        ]:
            label.setFont(QFont("Consolas", 11))
            status_layout.addWidget(label)
        self.status_box.setLayout(status_layout)
        layout.addWidget(self.status_box)
        
        # --- Toggles Layout ---
        toggles_layout = QHBoxLayout()
        toggles_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        toggles_layout.setSpacing(10)
        def create_toggle_box(label_text):
            box = QFrame()
            box.setStyleSheet("background-color: #2b2b3d; border-radius: 10px; padding: 3px;")
            box.setFixedSize(186, 75)
            vbox = QVBoxLayout()
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            label.setStyleSheet("color: #00ffcc;")
            toggle = ToggleSwitch()
            vbox.addWidget(label)
            vbox.addWidget(toggle, alignment=Qt.AlignmentFlag.AlignCenter)
            box.setLayout(vbox)
            return box, toggle
        auto_connect_box, self.auto_connect_toggle = create_toggle_box("Auto-Connect")
        ad_block_box, self.ad_block_toggle = create_toggle_box("Ad Block")
        toggles_layout.addWidget(auto_connect_box)
        toggles_layout.addWidget(ad_block_box)
        layout.addLayout(toggles_layout)
        self.auto_connect_toggle.toggled.connect(self.handle_auto_connect)
        self.ad_block_toggle.toggled.connect(self.handle_ad_block)
        self.auto_connect_toggle.toggled.connect(self.save_toggle_states)
        self.ad_block_toggle.toggled.connect(self.save_toggle_states)
        
        # --- Buttons ---
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(12)
        self.stop_button = QPushButton("Stop\nConnection")
        self.stop_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.stop_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4d;
                color: white;
                padding: 10px 50px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #e04343;
            }
        """)
        self.stop_button.clicked.connect(self.stop_connection)
        self.start_button = QPushButton("Start\nConnection")
        self.start_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #00c896;
                color: black;
                padding: 10px 50px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #00b586;
            }
        """)
        self.start_button.clicked.connect(self.start_connection)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.start_button)
        layout.addLayout(button_layout)
        main_widget.setLayout(layout)

    # ----- Tray Integration -----
    def init_tray(self):
        icon_path = self.resource_path("logo.ico")
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        tray_menu = QMenu()
        show_action = QAction("Restore", self)
        quit_action = QAction("Quit", self)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        show_action.triggered.connect(self.show_main_window)
        quit_action.triggered.connect(self.on_quit)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def on_tray_icon_activated(self, reason):
        if (reason == QSystemTrayIcon.ActivationReason.DoubleClick or
            reason == QSystemTrayIcon.ActivationReason.Trigger):
            self.show_main_window()

    def show_main_window(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def on_quit(self):
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.worker_thread.wait()  
        QApplication.instance().quit()


    def start_connection(self):
        if self.worker_thread is None or not self.worker_thread.isRunning():
            self.animation_status.setText("Connection started...")
            self.worker_thread = WorkerThread()
            self.worker_thread.progress.connect(self.update_status)
            self.worker_thread.start()
        else:
            self.animation_status.setText("Connection already running.")

    def stop_connection(self):
        if self.worker_thread and self.worker_thread.isRunning():
            self.animation_status.setText("Connection stopped.")
            self.wifi_status.setText("WiFi Status: Disconnected ❌")
            self.internet_status.setText("Internet: Disconnected ❌")
            self.user_status.setText("User: None")
            self.signal_status.setText("Signal Strength: ❗")
            self.worker_thread.stop()
        else:
            self.animation_status.setText("No active connection to stop.")

    def update_status(self, status, message):
        if status == "animation_status":
            self.animation_status.setText(message)
        elif status == "wifi_status":
            self.wifi_status.setText(f"WiFi Status: {message}")
        elif status == "internet_status":
            self.internet_status.setText(f"Internet: {message}")
        elif status == "user_status":
            self.user_status.setText(f"User: {message}")

    def handle_auto_connect(self, checked):
        if checked:
            self.animation_status.setText("Auto-Connect enabled")
        else:
            self.animation_status.setText("Auto-Connect disabled")

    def handle_ad_block(self, checked):
        if not is_admin():
            self.ad_block_toggle.setChecked(False)
            self.animation_status.setText("Run as Administrator for Ad-Block")
            return
        dns_servers = ["1.1.1.1", "8.8.8.8"]
        interfaces = []
        output, err, code = run_cmd_silently('netsh interface show interface', shell=True)
        if code != 0 or not output:
            self.ad_block_toggle.setChecked(False)
            self.animation_status.setText("Run as Administrator for Ad-Block")
            return
        for line in output.splitlines():
            if "Connected" in line:
                parts = line.split()
                if len(parts) >= 4:
                    interfaces.append(" ".join(parts[3:]))
        if not interfaces:
            self.ad_block_toggle.setChecked(False)
            self.animation_status.setText("No connected interfaces detected.")
            return
        if checked:
            try:
                for iface in interfaces:
                    cmd1 = f'netsh interface ip set dns name="{iface}" static {dns_servers[0]}'
                    out1, err1, code1 = run_cmd_silently(cmd1, shell=True)
                    if code1 != 0:
                        raise Exception(err1 or "Failed to set DNS")
                    if len(dns_servers) > 1:
                        cmd2 = f'netsh interface ip add dns name="{iface}" {dns_servers[1]} index=2'
                        out2, err2, code2 = run_cmd_silently(cmd2, shell=True)
                        if code2 != 0:
                            raise Exception(err2 or "Failed to add DNS")
                self.animation_status.setText("Ad Block enabled")
            except Exception as e:
                self.ad_block_toggle.setChecked(False)
                self.animation_status.setText("Run as Administrator for Ad-Block")
                return
        else:
            try:
                for iface in interfaces:
                    cmd = f'netsh interface ip set dns name="{iface}" source=dhcp'
                    out, err, code = run_cmd_silently(cmd, shell=True)
                    if code != 0:
                        raise Exception(err or "Failed to reset DNS")
                self.animation_status.setText("Ad Block disabled")
            except Exception as e:
                self.animation_status.setText("Some Error Occured !")
                return

    def save_toggle_states(self):
        self.settings.setValue("autoconnect", self.auto_connect_toggle.isChecked())
        self.settings.setValue("adblock", self.ad_block_toggle.isChecked())

    def restore_toggle_states(self):
        auto_state = self.settings.value("autoconnect", False, type=bool)
        adblock_state = self.settings.value("adblock", False, type=bool)
        self.auto_connect_toggle.setChecked(auto_state)
        self.ad_block_toggle.setChecked(adblock_state)
        if auto_state:
            QTimer.singleShot(0, self.start_connection)

    def closeEvent(self, event):
        # Save toggles, safely stop threads, and minimize to tray
        # if self.worker_thread and self.worker_thread.isRunning():
        #     # self.worker_thread.stop()
        self.save_toggle_states()
        # Minimize to tray instead of actually quitting
        event.ignore()
        self.hide()
        if self.tray_icon:
            self.tray_icon.showMessage(
                "NexOnet is running in tray",
                "Double-click the tray icon to restore.",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NexOnetGUI()
    window.show()
    sys.exit(app.exec())

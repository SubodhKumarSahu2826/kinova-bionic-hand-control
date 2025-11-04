# widget.py
import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtCore import Qt
from ui_form import Ui_Widget

# Add path to UART and Kinova SDK
sys.path.append(r"D:\\Kinova-kortex2_Gen3_G3L-Master\\Kinova-kortex2_Gen3_G3L-master\\api_python\\examples\\103-Gen3_uart_bridge")

from uart_bridge import UARTBridge
from kortex_api.RouterClient import RouterClient
from kortex_api.TCPTransport import TCPTransport
from kortex_api.SessionManager import SessionManager
from kortex_api.autogen.messages import Common_pb2, Session_pb2
from kortex_api.autogen.messages import InterconnectConfig_pb2

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.uart_bridge = None
        self.router = None
        self.transport = None
        self.session = None

        self.slider_values = {
            'Index': 0,
            'Middle': 0,
            'Thumb': 0,
            'Ring': 0
        }

        # Button connections
        self.ui.pushButton.clicked.connect(self.connect_robot)
        self.ui.pushButton_2.clicked.connect(self.disconnect_robot)
        self.ui.pushButton_3.clicked.connect(self.send_grip_open)
        self.ui.pushButton_4.clicked.connect(self.send_grip_close)

        # Slider connections
        self.ui.horizontalSlider.valueChanged.connect(lambda val: self.slider_changed(val, 'Index'))
        self.ui.horizontalSlider_2.valueChanged.connect(lambda val: self.slider_changed(val, 'Middle'))
        self.ui.horizontalSlider_3.valueChanged.connect(lambda val: self.slider_changed(val, 'Ring'))
        self.ui.horizontalSlider_4.valueChanged.connect(lambda val: self.slider_changed(val, 'Thumb'))

    def connect_robot(self):
        try:
            ip_address = "192.168.1.10"
            username = "admin"
            password = "admin"

            self.transport = TCPTransport()
            self.transport.connect(ip_address, 10000)

            self.router = RouterClient(self.transport, lambda k_err: print("Kortex error:", k_err))
            self.session = SessionManager(self.router)

            create_session_info = Session_pb2.CreateSessionInfo()
            create_session_info.username = username
            create_session_info.password = password
            create_session_info.session_inactivity_timeout = 60000
            create_session_info.connection_inactivity_timeout = 2000

            self.session.CreateSession(create_session_info)

            self.uart_bridge = UARTBridge(self.router, ip_address)
            self.uart_bridge.Configure(
                port_id=InterconnectConfig_pb2.UART_PORT_EXPANSION,
                enabled=True,
                speed=Common_pb2.UART_SPEED_115200,
                word_length=Common_pb2.UART_WORD_LENGTH_8,
                stop_bits=Common_pb2.UART_STOP_BITS_1,
                parity=Common_pb2.UART_PARITY_NONE
            )
            success = self.uart_bridge.EnableBridge()
            if not success:
                raise Exception("Failed to enable UART bridge.")
            QMessageBox.information(self, "Success", "Connected to Kinova Gen3")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    def disconnect_robot(self):
        try:
            if self.uart_bridge:
                try:
                    self.uart_bridge.DisableBridge()
                except Exception as e:
                    print(f"DisableBridge failed: {e}")
                try:
                    self.uart_bridge.Cleanup()
                except Exception as e:
                    print(f"Cleanup failed: {e}")
                self.uart_bridge = None
            if self.session:
                try:
                    self.session.CloseSession()
                except Exception as e:
                    print(f"CloseSession failed: {e}")
                self.session = None
            if self.transport:
                try:
                    self.transport.disconnect()
                except Exception as e:
                    print(f"Transport disconnect failed: {e}")
                self.transport = None
            QMessageBox.information(self, "Disconnected", "Disconnected from Kinova Gen3")
        except Exception as e:
            QMessageBox.critical(self, "Disconnect Error", str(e))

    def send_grip_open(self):
        if self.uart_bridge:
            try:
                self.uart_bridge.send_uart_command("2B 01 0A 02 00 00 23")
            except Exception as e:
                QMessageBox.critical(self, "UART Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "Not connected")

    def send_grip_close(self):
        if self.uart_bridge:
            try:
                self.uart_bridge.send_uart_command("2B 01 0A 01 00 00 23")
            except Exception as e:
                QMessageBox.critical(self, "UART Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "Not connected")

    def slider_changed(self, value, finger_name):
        print(f"{finger_name} slider value: {value}")
        if self.uart_bridge:
            self.slider_values[finger_name] = value

            if self.ui.radioButton_2.isChecked():  # Percentage Mode
                M1 = self.slider_values['Index']   # Byte 2
                M2 = self.slider_values['Middle']  # Byte 3
                M3 = self.slider_values['Thumb']   # Byte 4
                M4 = self.slider_values['Ring']    # Byte 5

                command_bytes = [0x2B, 0x02, M1, M2, M3, M4, 0x23]  # Byte 6 is constant 0x23
                hex_command = ' '.join(f"{b:02X}" for b in command_bytes)
                print(f"[Percentage Mode] Command: {hex_command}")
                try:
                    self.uart_bridge.send_uart_command(hex_command)
                except Exception as e:
                    print(f"Slider send error: {e}")
            else:
                print("[Normal Mode] Ignoring slider in normal mode")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.setWindowTitle("Kinova Gen3 Gripper Control")
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec())

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFrame
from PySide6.QtGui import QFont
from view.design import CircleIcon

class CommandWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Command Window")
        #self.setGeometry(100, 100, 400, 100)
        self.setMinimumWidth(280)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self._command_input = QLineEdit()
        self._command_input.setPlaceholderText("Enter command")
        self._command_input.setMinimumWidth(200)
        self.layout.addWidget(self._command_input)

        self._button = QPushButton("Send")
        self.layout.addWidget(self._button)

        self.adjustSize()
        
        self.layout.addStretch()

    def get_button(self):
        return self._button
    
    def get_command_input(self):
        return self._command_input

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def run(self):
        self.show()

class ConnectionsWindow(QWidget):
    def __init__(self, repository):
        super().__init__()

        self.setWindowTitle("Connections")
        #self.setGeometry(100, 100, 600, 400)
        self.setMinimumWidth(280)

        parent_layout = QVBoxLayout()
        self.setLayout(parent_layout)

        colours = {
            "online": "#1E90FF",
            "offline": "#FF0000",
            "connected": "#008000"
        }

        server_info_layout = QHBoxLayout()
        server_label = QLabel("Server")
        server_icon = CircleIcon(color=colours["connected"] if repository.is_server_connected() else colours["offline"])
        server_connection = QLabel("Connected" if repository.is_server_connected() else "Offline")
        server_info_layout.addWidget(server_label)
        server_info_layout.addWidget(server_icon)
        server_info_layout.addWidget(server_connection)

        server_connection_layout = QHBoxLayout()
        server_ip = QLineEdit("192.168.1.88:8082")
        connect_button = QPushButton("Connect")
        server_connection_layout.addWidget(server_ip)
        server_connection_layout.addWidget(connect_button)

        server_layout = QVBoxLayout()
        server_layout.addLayout(server_info_layout)
        server_layout.addLayout(server_connection_layout)

        parent_layout.addLayout(server_layout)

        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        parent_layout.addWidget(horizontal_line)

        devices_layout = QVBoxLayout()
        title = QLabel("Devices")
        title.setFont(QFont("Ubuntu", 16, QFont.Weight.Bold))
        devices_layout.addWidget(title)

        devices = repository.get_devices()
        for device, status in devices.items():
            device_layout = QHBoxLayout()
            device_label = QLabel(device)
            device_icon = CircleIcon(color=colours[status])
            device_connection = QLabel(str(status).capitalize())
            device_layout.addWidget(device_label)
            device_layout.addWidget(device_icon)
            device_layout.addWidget(device_connection)
            devices_layout.addLayout(device_layout)

        parent_layout.addLayout(devices_layout)

        parent_layout.addStretch()

        self.adjustSize()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def run(self):
        self.show()
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton

class CommandWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Command Window")
        self.setGeometry(100, 100, 400, 100)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self._command_input = QLineEdit()
        self._command_input.setPlaceholderText("Enter command")
        self.layout.addWidget(self._command_input)

        self._button = QPushButton("Send")
        self.layout.addWidget(self._button)

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
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connections")
        self.setGeometry(100, 100, 400, 100)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.connections = QLineEdit()
        self.connections.setPlaceholderText("Connections")
        self.layout.addWidget(self.connections)

    def run(self):
        self.show()
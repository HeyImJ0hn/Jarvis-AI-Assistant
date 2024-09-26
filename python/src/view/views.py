from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton

class CommandWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Command Window")
        self.setGeometry(100, 100, 400, 100)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command")
        self.command_input.returnPressed.connect(self.on_return_pressed)
        self.layout.addWidget(self.command_input)

        self.button = QPushButton("Send")
        self.button.clicked.connect(self.on_button_click)
        self.layout.addWidget(self.button)

    def on_button_click(self):
        command = self.command_input.text()
        self.command_input.clear()

        # Send the command to the controller
        self.controller.handle_button_click(command)

    def on_return_pressed(self):
        self.on_button_click()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def run(self):
        self.show()
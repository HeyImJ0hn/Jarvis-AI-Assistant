from view.views import CommandWindow, ConnectionsWindow

class CommandWindowController:
    def __init__(self):
        self._view = CommandWindow()
        self._model = None

        self._button = self._view.get_button()
        self._command_input = self._view.get_command_input()

        self._button.clicked.connect(self.handle_button_click)
        self._command_input.returnPressed.connect(self.handle_return_pressed)

    def handle_button_click(self):
        input = self._view.get_command_input()
        command = input.text()
        input.clear()
        # TODO: Send command to server

    def handle_return_pressed(self):
        self.handle_button_click()

    def run(self):
        self._view.run()

class ConnectionsWindowController:
    def __init__(self, repository):
        self._view = ConnectionsWindow(repository)
        self._model = None

    def run(self):
        self._view.run()
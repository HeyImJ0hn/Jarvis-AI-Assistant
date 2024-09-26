from view.views import CommandWindow
from controller.viewcontrollers import CommandWindowController

class TrayIconController:
    def __init__(self):
        self.command_window = None

    def send_command(self):
        command_window_controller = CommandWindowController()
        self.command_window = CommandWindow(command_window_controller)
        self.command_window.run()
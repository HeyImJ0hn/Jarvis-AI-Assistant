from controller.viewcontrollers import CommandWindowController
from view.trayicon import TrayIcon

class TrayIconController:
    def __init__(self):
        self.view = TrayIcon(self)
        self.command_window = None

    def send_command(self):
        self.command_window = CommandWindowController()
        self.command_window.run()

    def run(self):
        self.view.run()
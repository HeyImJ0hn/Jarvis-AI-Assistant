from controller.viewcontrollers import CommandWindowController, ConnectionsWindowController
from view.trayicon import TrayIcon
from model.network.client import Client
from model.repository.repository import Repository
import asyncio
import threading

class TrayIconController:
    def __init__(self):
        self.view = TrayIcon(self)
        self.command_window = None
        self.connections_window = None

        self.repository = Repository()

        self.client = Client('192.168.1.88', '8082', self.repository)
        self.loop_thread = threading.Thread(target=self.start_loop, daemon=True)
        self.loop_thread.start()

    def start_loop(self):
        asyncio.run(self.client.run())

    def send_command(self):
        self.command_window = CommandWindowController()
        self.command_window.run()

    def connections(self):
        self.connections_window = ConnectionsWindowController(self.repository)
        self.connections_window.run()

    def run(self):
        self.view.run()
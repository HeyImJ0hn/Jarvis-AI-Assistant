import asyncio
from model.network.client import Client

from controller.viewcontrollers import CommandWindowController
from view.views import CommandWindow
from view.trayicon import TrayIcon

from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    #client = Client('192.168.1.88', '8082')
    #asyncio.run(client.run())
    
    app = QApplication([])
    tray_icon = TrayIcon()
    
    tray_icon.run()
    app.exec()
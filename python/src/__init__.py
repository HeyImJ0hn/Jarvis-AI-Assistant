import asyncio
from model.network.client import Client

from controller.trayiconcontroller import TrayIconController

from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    #client = Client('192.168.1.88', '8082')
    #asyncio.run(client.run())
    
    app = QApplication([])
    tray_icon = TrayIconController()
    
    tray_icon.run()
    app.exec()
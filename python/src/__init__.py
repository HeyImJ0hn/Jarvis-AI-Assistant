from controller.trayiconcontroller import TrayIconController
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    tray_icon = TrayIconController()
    
    tray_icon.run()
    app.exec()
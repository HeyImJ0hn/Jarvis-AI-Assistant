import pystray
from PIL import Image
import sys

class TrayIcon:
    def __init__(self, controller):
        self.controller = controller

        self.image = Image.open("python/static/reactor.png")
        self.menu = pystray.Menu(
            pystray.MenuItem("J.A.R.V.I.S.", None, visible=True, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Command", self.send_command, visible=True, enabled=True),
            pystray.MenuItem("Connections", self.send_command, visible=True, enabled=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit, visible=True, enabled=True)
        )
        self.icon = pystray.Icon("J.A.R.V.I.S.", self.image, "J.A.R.V.I.S.", self.menu)

    def send_command(self):
        self.controller.send_command()

    def run(self):
        self.icon.run_detached()

    def quit(self):
        sys.exit(0)
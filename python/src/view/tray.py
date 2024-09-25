import pystray
from PIL import Image

class Tray:
    def __init__(self):
        self.image = Image.open("python/static/reactor.png")
        self.menu = pystray.Menu(
            pystray.MenuItem("J.A.R.V.I.S.", lambda: print("e"), visible=True, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self.exit, visible=True, enabled=True)
        )
        self.icon = pystray.Icon("J.A.R.V.I.S.", self.image, "J.A.R.V.I.S.", self.menu)

    def run(self):
        self.icon.run()

    def exit(self):
        self.icon.stop()

if __name__ == '__main__':
    tray = Tray()
    tray.run()
class Repository:
    def __init__(self):
        self._server_ip = ""
        self._server_connected = False
        self._devices = {}

    def process_status_update(self, data):
        self._server_connected = True
        for device, status in data["status"].items():
            self._devices[device] = status

    def get_devices(self):
        return self._devices
    
    def get_server_ip(self):
        return self._server_ip
    
    def set_server_ip(self, ip):
        self._server_ip = ip

    def is_server_connected(self):
        return self._server_connected
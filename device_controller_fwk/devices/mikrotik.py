from device_controller_fwk.devices import Device


class Mikrotik(Device):

    def __init__(self, ip, user, password):
        super().__init__(ip, user, password)

    def shutdown(self):
        self.exec_command("system shutdown")

    def beep(self):
        self.exec_command("beep")

    def blink(self, duration=5):
        self.exec_command(f"blink duration={duration}")
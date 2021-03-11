import subprocess


class Controller:

    def get_hostname(self):
        return subprocess.run(['hostname'])

    def get_ip(self):
        return subprocess.run(["hostname -I"])

    def get_battery_status(self):
        return subprocess.run(["acpaccess"])

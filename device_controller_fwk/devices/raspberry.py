from device_controller_fwk.devices import Device


class RaspberryPi(Device):
    def __init__(self, ip, user, password):
        super().__init__(ip, user, password)

    def reboot(self):
        self.exec_command("sudo reboot")

    def shutdown(self, now=False):
        cmd = "sudo shutdown"
        if now:
            cmd += " now"
        self.exec_command(cmd)

    def update(self):
        stdout, stderr = self.exec_command("sudo apt update && sudo apt upgrade -y")
        print(stdout.readlines())
        # stdin1, stdout1, stderr1 = self.ssh.exec_command(self.password)

    def ping(self, host, count=4):
        stdout, stderr = self.exec_command(f"ping {host} -c {count}")
        print(stdout.readlines())

    def get_battery_status(self):
        stdout, stderr = self.exec_command("apcaccess")
        print(stdout.readlines())
        print(stderr.readlines())

    def get_hostname(self):
        stdout, stderr = self.exec_command("hostname")
        print(stdout.readlines())

    def get_host_ip(self, host):
        stdout, stderr = self.exec_command(f"dig {host}")
        print(stdout.readlines())

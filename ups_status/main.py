import paramiko
import yaml
import contextlib

# TODO connect using private - public keys
# TODO open connection and maintain it open till the script has ended
# TODO add logger and send - receive logic for debugging
# TODO add webserver for storing run logs and other information
# TODO structure the code in modules
# TODO implement verification check if command has succeeded
# TODO make as many commands as possible for each device
# TODO add sql database for storing logs


class YamlLoad:

    def __init__(self, file, device_class, device, mode="r"):
        self.file = file
        self.device_class = device_class
        self.device = device
        self._file_content = open(file, mode)
        self._file_dict = yaml.load(self._file_content, Loader=yaml.FullLoader)
        self.ip = self._file_dict["devices"][device_class][device]["ip"]
        self.user = self._file_dict["devices"][device_class][device]["user"]
        self.password = self._file_dict["devices"][device_class][device]["password"]
        self._file_content.close()


class Device:

    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    @contextlib.contextmanager
    def connect(self):
        self.ssh.connect(self.ip, username=self.user, password=self.password)
        yield
        self.ssh.close()

    def exec_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout, stderr


class Mikrotik(Device):

    def __init__(self, ip, user, password):
        super().__init__(ip, user, password)

    def shutdown(self):
        self.exec_command("system shutdown")

    def beep(self):
        self.exec_command("beep")

    def blink(self, duration=5):
        self.exec_command(f"blink duration={duration}")


class RaspberryPi(Device):
    def __init__(self, ip, user, password):
        super().__init__(ip, user, password)

    def reboot(self):
        self.exec_command("sudo reboot")

    def shutdown(self):
        self.exec_command("sudo shutdown now")

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


# router_info = YamlLoad("devices.yaml", "lan_devices", "router")
# router = Mikrotik(router_info.ip, router_info.user, router_info.password)
# router.beep()

# rpi1 = YamlLoad("devices.yaml", "servers", "rpi1")
# rpi1 = RaspberryPi(rpi1.ip, rpi1.user, rpi1.password)
# rpi1.get_history()

# rpi2 = YamlLoad("devices.yaml", "servers", "rpi2")
# rpi2 = RaspberryPi(rpi2.ip, rpi2.user, rpi2.password)
# rpi2.ping("google.com")

nas_server = YamlLoad("devices.yaml", "servers", "nas-server")
nas_server = RaspberryPi(nas_server.ip, nas_server.user, nas_server.password)
with nas_server.connect():
    nas_server.ping("google.com")
    nas_server.get_hostname()
    nas_server.get_host_ip("google.com")

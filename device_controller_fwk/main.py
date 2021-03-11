from device_controller_fwk.info_loader import YamlLoad
from device_controller_fwk.devices.raspberry import RaspberryPi
from device_controller_fwk.devices.mikrotik import Mikrotik
from device_controller_fwk.devices.controller import Controller

# TODO connect using private - public keys
# TODO open connection and maintain it open till the script has ended
# TODO add logger and send - receive logic for debugging
# TODO add webserver for storing run logs and other information
# TODO structure the code in modules
# TODO implement verification check if command has succeeded
# TODO make as many commands as possible for each device
# TODO add sql database for storing logs

controller = Controller()
controller.get_battery_status()

# router_info = YamlLoad("devices.yaml", "lan_devices", "router")
# router = Mikrotik(router_info.ip, router_info.user, router_info.password)
# with router.connect():
#     router.beep()

# rpi1 = YamlLoad("devices.yaml", "servers", "rpi1")
# rpi1 = RaspberryPi(rpi1.ip, rpi1.user, rpi1.password)
# rpi1.get_history()

# rpi2 = YamlLoad("devices.yaml", "servers", "rpi2")
# rpi2 = RaspberryPi(rpi2.ip, rpi2.user, rpi2.password)
# rpi2.ping("google.com")

# nas_server_info = YamlLoad("devices.yaml", "servers", "nas-server")
# nas_server = RaspberryPi(nas_server_info.ip, nas_server_info.user, nas_server_info.password)
# with nas_server.connect():
    # nas_server.get_hostname()
    # nas_server.get_host_ip("google.com")
    # nas_server.get_battery_status()



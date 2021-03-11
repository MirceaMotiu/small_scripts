import yaml


class YamlLoad:

    def __init__(self, file, device_class, device, mode="r"):
        self.file = file
        self.device_class = device_class
        self.device = device
        self._file_content = open(self.file, mode)
        self._file_dict = yaml.load(self._file_content, Loader=yaml.FullLoader)
        self.ip = self._file_dict[self.device_class][self.device]["ip"]
        self.user = self._file_dict[self.device_class][self.device]["user"]
        self.password = self._file_dict[self.device_class][self.device]["password"]
        self._file_content.close()

import paramiko
import contextlib


class Device:

    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()

    @contextlib.contextmanager
    def connect(self):
        self.ssh.connect(self.ip, username=self.user, allow_agent=True)
        yield
        self.ssh.close()

    def exec_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout, stderr


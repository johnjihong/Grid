import paramiko
from .log import logger


class ParamikoClient(paramiko.SSHClient):
    def __init__(self, username: str, password: str, hostname: str, port: int=22):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        super().__init__()

    def connect(self):
        try:
            self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            super().connect(self.hostname, port=self.port, username=self.username, password=self.password)
        except paramiko.AuthenticationException:
            logger.exception(exc_info=True)
        else:
            logger.info('%s connected to the %s.' % (self.username, self.hostname))

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

import getpass
from telnetlib import Telnet
import logging

logging.basicConfig(level=logging.DEBUG)


class TelnetParserRouter(Telnet):

    def __init__(self):
        super().__init__()

    def connect_router(self, host: str):
        try:
            self.open(host)
            logging.info(f"Подключились к роутеру с ip: {host}")
        except:
            logging.error(f"Не смогли подключиться к роутеру {host}")
            raise

    @staticmethod
    def convert_bytes(st: str) -> bytes:

        return bytes(st, encoding="ascii")

    def login_router(self,  login: str, password: str):

        logging.info("Логинимся")
        self.write(login.encode("ascii") + b"\n")
        self.write(password.encode("ascii") + b"\n")

    def login_admin(self, secret_password: str):

        logging.info("Переходим в привилегированный режим")
        self.write(b"enable\n")
        self.write(self.convert_bytes(secret_password+"\n"))

    def send_command(self, command: str):
        self.write(b"\n")
        self.write(self.convert_bytes(command+"\n"))
        self.write(b"\n")

    def get_info(self, read_to: str) -> str:
        """Считать из ответного потока"""

        return self.read_until(self.convert_bytes(read_to), timeout=5).decode("ascii")

    def get_version_router(self) -> str:

        self.send_command("show version")
        self.get_info("#show version")
        out = self.get_info("Configuration register")
        self.get_info("#")
        return out[out.find('Version'): out.find('RELEASE')-2]

    def get_start_configuration(self):

        self.send_command("show startup-config")
        self.get_info("#show startup-config")
        config = self.get_info("end\n")
        config = self.clean_string(config[config.find('Using'):config.find('\nend\r')])
        self.get_info("#")
        return config

    def clean_string(self, txt: str) -> str:

        return txt.replace('\r', '').replace('!', '').replace('\n\nend', '').replace('\n\n\n', '\n')\
            .replace('\n\n\nend', '').replace("\n\n\n\n", "\n\n").replace('\n\n\n', '\n')

    def get_current_configuration(self):

        self.send_command("show running-config")
        self.get_info("#show running-config")
        config = self.get_info("end\n")
        config = self.clean_string(config[config.find('Current'):config.find('\nend\r')])
        self.get_info("#")
        return config

    def get_interface_info(self):

        self.send_command("show interface")
        self.get_info("#show interface")
        config = self.get_info('#')
        return self.clean_string(config[:-3])

    def get_acl_info(self):
        self.send_command("show access-lists")
        self.get_info("#show access-lists")
        config = self.get_info('#')
        config = self.clean_string(config)
        return 'Нет настроек доступа' if 'IP' not in config else config

    def close_connect(self):

        logging.info("Закрываем соединение")
        self.write(b"end\n")
        self.write(b"\n")
        self.write(b"exit\n")
        self.close()
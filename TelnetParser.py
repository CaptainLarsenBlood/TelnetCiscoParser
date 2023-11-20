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

        return self.read_until(self.convert_bytes(read_to), timeout=5).decode("ascii")

    def close_connect(self):

        logging.info("Закрываем соединение")
        self.write(b"end\n")
        self.write(b"\n")
        self.write(b"exit\n")
        self.close()
from TelnetParser import TelnetParserRouter
import logging
logging.basicConfig(level=logging.DEBUG)

host = '10.1.1.3'
username = "R1"
password = "12345"
secret_pas = "cisco"


if __name__ == '__main__':

    logging.info("Подключаем к хосту")
    telnet_client = TelnetParserRouter()
    telnet_client.connect_router(host)
    telnet_client.login_router(username, password)
    telnet_client.login_admin(secret_pas)

    logging.info("Собираем информацию о роутере")
    telnet_client.send_command("terminal length 0")
    print("Версия коммутатора: %s\n" % (telnet_client.get_version_router("Technical Support")))
    print("Стартовая конфигурация:\n\n%s\n" % telnet_client.get_start_configuration())
    print("Текущая конфигурация:\n\n%s\n" % telnet_client.get_current_configuration())
    telnet_client.close_connect()

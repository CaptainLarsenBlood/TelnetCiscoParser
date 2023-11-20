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
    print("ВЕРСИЯ КОММУТАТОРА: %s\n" % (telnet_client.get_version_router()))
    print("СТАРТОВАЯ КОНФИГУРАЦИЯ:\n\n%s\n" % telnet_client.get_start_configuration())
    print("ТЕКУЩАЯ КОНФИГУРАЦИЯ:\n\n%s\n" % telnet_client.get_current_configuration())
    print("ИНТЕРФЕЙСЫ:\n %s\n" % telnet_client.get_interface_info())
    print("СВЕДЕНИЯ О СПИСКАХ КОНТРОЛЯ ДОСТУПА (ACL) КОММУТАТОРА:\n %s \n" % telnet_client.get_acl_info())
    telnet_client.close_connect()

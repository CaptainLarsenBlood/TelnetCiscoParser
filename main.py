from TelnetParser import TelnetParserRouter

host = '10.1.1.3'
username = "R1"
password = "12345"
secret_pas = "cisco"


if __name__ == '__main__':
    telnet_client = TelnetParserRouter()
    telnet_client.connect_router(host)
    telnet_client.login_router(username, password)
    telnet_client.login_admin(secret_pas)
    telnet_client.send_command("terminal length 0")
    telnet_client.send_command("show startup-config")
    startup_info = telnet_client.get_info("end")
    telnet_client.send_command("show running-config")
    running_info = telnet_client.get_info("end\n")
    telnet_client.send_command("show version")
    router_info = telnet_client.get_info("Technical Support")
    telnet_client.close_connect()

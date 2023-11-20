import getpass
import telnetlib

HOST = '10.1.1.3'
user = "R1"
password = "12345"
print('Successfully passed getpass')
tn = telnetlib.Telnet(HOST)
print('Successfully passed telnet')
tn.read_until(b"Username:")
tn.write(user.encode("ascii") + b"\n")

tn.read_until(b"Password:")
tn.write(password.encode("ascii")+b"\n")

tn.write(b"show startup-config\n")
tn.write(b"end\n")
tn.write(b"\n")
tn.write(b"exit\n")
res = tn.read_all().decode("ascii")
print(res)
res = res.split(',')
model_router = res[1].strip()
version = res[2].strip()

print(res)

123

from netmiko import ConnectHandler

switch = {
    'device_type': 'cisco_nxos',
    'ip': '10.10.20.177',
    'username': 'cisco',
    'password': 'cisco123'
}

net_connect = ConnectHandler(**switch)
output = net_connect.send_command("disable interface Eth1/17")
print(output)
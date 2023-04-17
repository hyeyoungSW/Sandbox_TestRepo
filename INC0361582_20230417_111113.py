

import netmiko

my_device = {
    'device_type': 'cisco_nxos',
    'ip': '10.10.20.177',
    'username': 'cisco',
    'password': 'cisco',
    'port': 22
 }

net_connect = netmiko.ConnectHandler(**my_device)

config_commands = ['interface eth1/7', 'switchport access vlan 5']
output = net_connect.send_config_set(config_commands)

print(output)
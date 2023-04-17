

from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type='cisco_nxos',
    ip='10.10.20.177',
    port=22,
    username='cisco',
    password='cisco')

net_connect.find_prompt()

output = net_connect.send_command('show run int eth1/7')
print(output)

config_commands = ['interface eth1/7', 'vlan 5']
output = net_connect.send_config_set(config_commands)
print(output)
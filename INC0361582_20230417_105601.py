

from netmiko import ConnectHandler

switch = {
    'device_type': 'cisco_nxos',
    'ip': '10.10.20.177',
    'username': 'cisco',
    'password': 'cisco'
}

net_connect = ConnectHandler(**switch)
output = net_connect.send_command_timing('conf t')
if output.strip().endswith('#'):
    command = 'interface eth1/7'
    command = command + '\n vlan 5'
    output = net_connect.send_command_timing(command)
    print(output)
else:
    print('Failed to get privileged exec mode')
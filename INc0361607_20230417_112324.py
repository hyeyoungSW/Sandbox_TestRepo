

from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type="cisco_nxos",
    ip="10.10.20.177",
    username="cisco",
    password="cisco",
)

net_connect.send_command_timing(
    "conf t\nint eth1/17\nno shut\nend\n", strip_command=False, strip_prompt=False
)

output = net_connect.send_command("show run int eth1/17", use_textfsm=True)
print(output)
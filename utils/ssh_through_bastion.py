from netmiko import ConnectHandler
from paramiko import SSHClient, AutoAddPolicy
from dataclasses import dataclass

@dataclass
class ConnectionInfo:
    username: str
    password: str
    ip_address: str
    device_type: str

def get_connection(self, device: ConnectionInfo, bastion: ConnectionInfo = None):
    switch = {
        'host': device.ip_address,
        'username': device.username,
        'key': device.password,
        'secret': device.password,
        'device_type': device.device_type
    }
    
    if bastion:
        bastion = {
            'host': bastion.ip_address,
            'username': bastion.username,
            'key': bastion.password,
            'device_type': 'linux', # Assuming bastion is a Linux server
            'port': 22
        }

        print(f"Connecting to bastion {bastion['host']}...")
        bastion_client = SSHClient()
        bastion_client.set_missing_host_key_policy(AutoAddPolicy())
        #bastion_client.connect(**bastion)
        bastion_client.connect(hostname=bastion['host'], username=bastion['username'], password=bastion['key'], port=bastion['port'])
        print("Successfully connected to bastion")

        print(f"Opening channel to switch {device.ip_address}...")
        bastion_transport = bastion_client.get_transport()
        dest_addr = (device.ip_address, 22)
        local_addr = ('127.0.0.1', 0) # Bind to any port on the local host
        bastion_channel = bastion_transport.open_channel("direct-tcpip", dest_addr, local_addr)
        switch['host'] = '127.0.0.1'
        switch['sock'] = bastion_channel
        print("Successfully opened channel to switch through bastion")


    self.net_connect = ConnectHandler(**switch)
    # Enter privileged mode (enable)
    self.net_connect.enable()
    self.ip = device.ip_address
    return self.net_connect
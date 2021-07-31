import socket
import re
import os

def bytes_sizeof_fmt(num, factor=1024.0, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < factor:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= factor
    return "%.1f%s%s" % (num, 'Yi', suffix)



def checkServerPort(port, protocol):
    server = os.environ["SERVER_ADDRESS"]
    ipaddress = socket.gethostbyname(server)
    if protocol == 'tcp':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # res = sock.sendto('PING', (ipaddress, port))
        return 'unknown'
    sock.settimeout(0.2)
    result = sock.connect_ex((ipaddress, int(port)))
    if result == 0:
        socket_status = 'open'
    else:
        socket_status = 'closed'
    sock.close()
    return socket_status
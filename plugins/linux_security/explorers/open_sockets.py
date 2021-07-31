import re
from core import ExplorerClass
from utils import checkServerPort


class Explorer(ExplorerClass):

    @classmethod
    def work(cls, output):
        params = []
        for string in output.split('\n'):
            if string:
                try:
                    protocol = re.findall(r'^(\w+)\s', string)[0]
                    socket_string = re.findall(r'^\w+\s([\d\.:]+)', string)[0]
                    ipv4, port = socket_string.split(':')
                    port_status = checkServerPort(int(port), protocol)
                    params.append({
                        'status': 'ok',
                        'name': protocol + ' ' + ipv4 + ':' + port,
                        'value': ipv4 + '-' + port_status,
                        'pretty_value': port_status,
                        'warnings': ["'open' in value", "'127.0.0.1' not in value"],
                    })
                except:
                    continue
        return params


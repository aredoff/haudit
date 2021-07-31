import re
from core import ExplorerClass
from utils import bytes_sizeof_fmt


class Explorer(ExplorerClass):

    @classmethod
    def work(cls, output):
        params = []
        for string in output.split('\n'):
            try:
                disk_name = re.findall(r'^(\S+)\s', string)[0]
                disk_size = re.findall(r'^\S+\s(\S+)\s', string)[0]
                disk_free = re.findall(r'^\S+\s\S+\s(\S+)\s', string)[0]
                disk_perc= re.findall(r'\s(\S+)%$', string)[0]
                params.append({
                    'status': 'ok',
                    'name': disk_name + ' size',
                    'value': disk_size,
                })
                params.append({
                    'status': 'ok',
                    'name': disk_name + ' free',
                    'value': disk_free,
                })
                params.append({
                    'status': 'ok',
                    'name': disk_name + ' usage',
                    'pretty_value': str(disk_perc) + '%',
                    'value': str(disk_perc),
                    'warnings': ['value>90'],
                })
            except:
                continue
        return params


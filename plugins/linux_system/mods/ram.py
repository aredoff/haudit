from core import ModClass
from utils import bytes_sizeof_fmt

class Mod(ModClass):

    @classmethod
    def work(cls, params):
        for param in params:
            if param['name'] == 'MemTotal':
                param['value'] = bytes_sizeof_fmt(int(param['value']) * 1000)
            if param['name'] == 'MemFree':
                param['value'] = bytes_sizeof_fmt(int(param['value']) * 1000)
            if param['name'] == 'MemAvailable':
                param['value'] = bytes_sizeof_fmt(int(param['value']) * 1000)

        return params


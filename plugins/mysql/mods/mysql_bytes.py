from core import ModClass
from utils import bytes_sizeof_fmt

class Mod(ModClass):
    @classmethod
    def work(cls, params):
        for param in params:
            if param['name'] == 'innodb_buffer_pool_size':
                param['pretty_value'] = bytes_sizeof_fmt(int(param['value']))
            if param['name'] == 'innodb_log_file_size':
                param['pretty_value'] = bytes_sizeof_fmt(int(param['value']))
            if param['name'] == 'innodb_log_buffer_size':
                param['pretty_value'] = bytes_sizeof_fmt(int(param['value']))
            if param['name'] == 'tmp_table_size':
                param['pretty_value'] = bytes_sizeof_fmt(int(param['value']))
            if param['name'] == 'max_heap_table_size':
                param['pretty_value'] = bytes_sizeof_fmt(int(param['value']))
            if param['name'] == 'join_buffer_size':
                param['pretty_value'] = bytes_sizeof_fmt(int(param['value']))
            if param['name'] == 'sort_buffer_size':
                param['pretty_value'] = bytes_sizeof_fmt(int(param['value']))
            if param['name'] == 'max_allowed_packet':
                param['pretty_value'] = bytes_sizeof_fmt(int(param['value']))
        return params


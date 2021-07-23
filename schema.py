data = {}
import json


data['queries'] = [{
    'command': 'string',
    'parameters': [
        {
            'name': 'string',
            'regex': 'regex',
            'normal_states': ['value',],
            'warn_states': ['value'],
        },
    ]
},]


with open('schema.json', 'w') as f:
    f.write(json.dumps(data))
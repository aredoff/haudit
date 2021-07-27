import re
import ast


def import_class_from_file(file, classname):
    module = __import__(file, fromlist=[classname])
    return getattr(module, classname)

#Модифицирует params
class ModClass():
    @classmethod
    def work(cls, params):
        return params


    @classmethod
    def prework(cls, queryReport):
        if 'params' in queryReport and queryReport['status'] == 'ok':
            return cls.work(queryReport['params'])
        else:
            return queryReport

#Преобразует текст в params
class ExplorerClass():
    @classmethod
    def work(cls, output):
        return output

    @classmethod
    def prework(cls, output):
        if output:
            return cls.work(output)
        else:
            return output


class FilterClass():
    def __init__(self):
        pass


class Validator():
    @classmethod
    def validate(cls, val, formula):
        try:
            value = cls.typeСast(val)
            _warningResult = eval(formula)
            if _warningResult:
                return False
            else:
                return True
        except:
            print('Error eval in:', val, '->', formula)
            exit()

    @classmethod
    def typeСast(cls, value):
        try:
            return ast.literal_eval(value) #num
        except:
            return value #str


class Parametr():
    def __init__(self, name: str, regex: str, category: str = None, warnings: list = None, value: str = None):
        self.name = name
        self.category = category
        self.regex = re.compile(regex)
        self.value = None
        self.baseunit = None
        if warnings:
            self.warnings = warnings
        else:
            self.warnings = []

    def __str__(self):
        return 'Plugin(' + self.name + ')'

    def __repr__(self):
        return 'Plugin(' + self.name + ')'

    def find(self, text):
        _ = self.regex.findall(text)
        if _:
            return _[0]
        else:
            return None





class Query():
    def __init__(self, **kwargs):
        self.category = kwargs['category']
        self.command = kwargs['command']
        self.params = []
        self.mods = []
        self.explorers = []

    def __str__(self):
        return 'Plugin(' + self.name + ',' + self.command + ')'

    def __repr__(self):
        return 'Plugin(' + self.name + ',' + self.command + ')'

    def adMod(self, path):
        self.mods.append(import_class_from_file(path, "Mod"))

    def adExplorer(self, path):
        self.explorers.append(import_class_from_file(path, "Explorer"))

    def run(self, sshClient):
        self.report = {
            'status': 'ok',
            'params': []
        }
        command_output = sshClient.execute_command(self.command)
        if command_output:
            for parameter in self.params:
                parameter_regex = parameter.findall(command_output)
                if parameter_regex:
                    self.report['params'].append({
                        'status': 'ok',
                        'name': parameter['name'],
                        'value': parameter_regex,
                    })
                else:
                    self.report['params'].append({
                        'status': 'error',
                        'name': parameter['name'],
                    })
        else:
            self.report['status'] = 'error'
        return self.report





class Plugin():
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.queries: [Query] = []

    def __str__(self):
        return 'Plugin(' + self.name + ')'

    def __repr__(self):
        return 'Plugin(' + self.name + ')'

    def execute(self, sshClient):
        self.report = []
        for query in self.queries:
            self.report.append(query.run(sshClient))


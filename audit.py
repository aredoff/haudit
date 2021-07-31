import os
import json
from ssh import SSHUtil
from core import Plugin, Query, Parametr, Validator
from rich.console import Console
from rich.table import Column, Table
from rich.panel import Panel
from pdf import PdfPrinter


class Audit():
    plugins_folder = 'plugins'
    console = Console()

    def __init__(self, ssh_client: SSHUtil):
        self.sshClient = ssh_client
        self.plugins = []
        for plugin_folder in os.listdir(self.plugins_folder):
            plugin = Plugin(name=plugin_folder, path=self.plugins_folder + '/' + plugin_folder)

            for file in os.listdir(plugin.path):
                if file.endswith('.json'):
                    with open(os.path.join(plugin.path, file), 'r') as f:
                        plugin_jsons_data = json.loads(f.read())
                        if 'queries' in plugin_jsons_data:
                            for query in plugin_jsons_data['queries']:
                                if 'command' in query:
                                    _q = Query(category=query['category'], command=query['command'])
                                elif 'input' in query:
                                    _q = Query(category=query['category'], input=query['input'])
                                else:
                                    print('File:{} Error: In query mast be "command" or "input"!'.format(file))
                                    exit()
                                if 'params' in query:
                                    for param in query['params']:
                                        _p = Parametr(name=param['name'], regex=param['regex'])
                                        if 'category' in param:
                                            _p.category = param['category']
                                        if 'warnings' in param:
                                            _p.warnings = param['warnings']
                                        if 'baseunit' in param:
                                            _p.baseunit = param['baseunit']
                                        _q.params.append(_p)
                                if 'mods' in query:
                                    for mod in query['mods']:
                                        _q.adMod('plugins.' + plugin_folder + '.mods.' + mod)
                                if 'explorers' in query:
                                    for explorer in query['explorers']:
                                        _q.adExplorer('plugins.' + plugin_folder + '.explorers.' + explorer)

                                plugin.queries.append(_q)
            self.plugins.append(plugin)


    def printReport(self, plugins_report):
        # print(plugins_report)
        # exit()

        self.console.print("[bold red on white]                                  ")
        self.console.print("[bold white on red]               Audit              ")
        self.console.print("[bold red on white]                                  ")

        for plugin_report in plugins_report:
            queries_table = Table(show_header=True, header_style="bold magenta")
            queries_table.add_column("Category")
            queries_table.add_column("Parametr")
            queries_table.add_column("Value")
            for query in plugin_report['queries']:
                for parametr in query['params']:
                    if parametr['status'] == 'ok':
                        if 'pretty_value' in parametr:
                            value = parametr['pretty_value']
                        else:
                            value = parametr['value']

                        if not parametr['validate']:
                            value = "[yellow]{}[/yellow]".format(value)
                    else:
                        value = "[red]Error[/red]"
                    category = query['category']
                    if 'category' in parametr:
                        if parametr['category']:
                            category = parametr['category']
                    queries_table.add_row(
                        category,
                        parametr['name'],
                        value,
                    )
            if queries_table.rows:
                self.console.print(Panel.fit(queries_table, title=plugin_report['name']))
            else:
                self.console.print("[red][Plugin <{}> did not receive data][/red]".format(plugin_report['name']))


    def printPdfReport(self, plugins_report, path_pdf_file):
        pdf = PdfPrinter()
        table_report = []
        for plugin_report in plugins_report:
            table_plugin_report = {
                'name': plugin_report['name'],
                'parametres': []
            }
            for query in plugin_report['queries']:
                for parametr in query['params']:
                    if parametr['status'] == 'ok':
                        if 'pretty_value' in parametr:
                            value = parametr['pretty_value']
                        else:
                            value = parametr['value']

                        if not parametr['validate']:
                            value = "<span class='warning'><b>{}</b></span>".format(value)
                        category = query['category']
                        if 'category' in parametr:
                            if parametr['category']:
                                category = parametr['category']
                        table_plugin_report['parametres'].append({
                            'category': category,
                            'name': parametr['name'],
                            'value': value,
                        })

            if table_plugin_report['parametres']:
                table_report.append(table_plugin_report)

        pdf.print(table_report, path_pdf_file)



    def execute_queries(self):
        self.plugins_report = []
        for plugin in self.plugins:
            plugin_report = {
                'name': plugin.name,
                'queries': [],
            }
            for query in plugin.queries:
                if query.command:
                    command_output = self.sshClient.execute_command(query.command)
                elif query.input:
                    file_path = os.path.abspath('plugins/{}/inputs/{}'.format(plugin.name, query.input))
                    command_output = self.sshClient.execute_file(file_path)
                else:
                    print('Error, query have not command or input')
                    exit()
                query_report = {
                    'status': 'ok',
                    'category': query.category,
                    'params': []
                }
                if command_output:
                    for parameter in query.params:
                        value = parameter.find(command_output)
                        if value:
                            _param_report = {
                                'status': 'ok',
                                'name': parameter.name,
                                'category': parameter.category,
                                'value': value,
                            }
                            if parameter.warnings:
                                _param_report['warnings'] = parameter.warnings
                            if parameter.baseunit:
                                _param_report['baseunit'] = parameter.baseunit
                            query_report['params'].append(_param_report)
                        else:
                            query_report['params'].append({
                                'status': 'error',
                                'category': parameter.category,
                                'name': parameter.name,
                            })

                    if query.explorers:
                        for explorer in query.explorers:
                            query_report['params'].extend(explorer.prework(command_output))

                    if query.mods:
                        for mod in query.mods:
                            mod.prework(query_report)
                else:
                    query_report['status'] = 'error'

                for param in query_report['params']:
                    if param['status'] == 'ok':
                        param['validate'] = True
                        if 'warnings' in param:
                            for warning in param['warnings']:
                                try:
                                    validate = Validator.validate(param['value'], warning)
                                    if not validate:
                                        param['validate'] = False
                                        break
                                except:
                                    print('Error eval in:', plugin.name,param['name'], param['value'], '->', warning)
                                    exit()


                plugin_report['queries'].append(query_report)
            self.plugins_report.append(plugin_report)
        return self.plugins_report





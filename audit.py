import os
import json
from ssh import SSHUtil
from core import Plugin, Query, Parametr
from rich.console import Console
from rich.table import Column, Table
from rich.panel import Panel


class Audit():
    plugins_folder = 'plugins'
    console = Console()

    def __init__(self, hostname, username, password):
        self.sshClient = SSHUtil(hostname=hostname, username=username, password=password)
        self.plugins = []
        for plugin_folder in os.listdir(self.plugins_folder):
            plugin = Plugin(name=plugin_folder, path=self.plugins_folder + '/' + plugin_folder)

            for file in os.listdir(plugin.path):
                if file.endswith('.json'):
                    with open(os.path.join(plugin.path, file), 'r') as f:
                        plugin_jsons_data = json.loads(f.read())
                        if 'queries' in plugin_jsons_data:
                            for query in plugin_jsons_data['queries']:
                                _q = Query(name=query['name'], command=query['command'])
                                if 'params' in query:
                                    for param in query['params']:
                                        _p = Parametr(name=param['name'], regex=param['regex'])
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
                        value = parametr['value']
                    else:
                        value = "[red]Error[/red]"
                    queries_table.add_row(
                        query['name'],
                        parametr['name'],
                        value,
                    )

            self.console.print(Panel.fit(queries_table, title=plugin_report['name']))


    def execute_queries(self):
        self.plugins_report = []
        for plugin in self.plugins:
            plugin_report = {
                'name': plugin.name,
                'queries': [],
            }
            for query in plugin.queries:
                command_output = self.sshClient.execute_command(query.command)
                query_report = {
                    'status': 'ok',
                    'name': query.name,
                    'params': []
                }
                if command_output:
                    for parameter in query.params:
                        parameter_regex_result = parameter.findall(command_output)
                        if parameter_regex_result:
                            query_report['params'].append({
                                'status': 'ok',
                                'name': parameter.name,
                                'value': parameter_regex_result,
                            })
                        else:
                            query_report['params'].append({
                                'status': 'error',
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
                plugin_report['queries'].append(query_report)
            self.plugins_report.append(plugin_report)
        return self.plugins_report





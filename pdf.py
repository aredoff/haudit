from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
import time

class PdfPrinter():
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('sources'))
        self.report_template = self.env.get_template("report_tmpl.html")
        self.css_file = "sources/typography.css"

    def _values_separator(self, table_data):
        sepurator_number = 40
        for plugin_report in table_data:
            for parametr in plugin_report['parametres']:
                if len(parametr['value']) > sepurator_number:
                    separator_itam_list = [parametr['value'][i:i+sepurator_number] for i in range(0, len(parametr['value']), sepurator_number)]
                    parametr['value'] = '\n'.join(separator_itam_list)
        return table_data

    def print(self, table_data, output_file):
        table_data = self._values_separator(table_data)
        created_time = time.strftime('%Y-%m-%d %H:%M')
        server = os.environ["SERVER_ADDRESS"]
        html_out = self.report_template.render(plugins_report=table_data, server_name=server, created_time=created_time)
        HTML(string=html_out).write_pdf(output_file, stylesheets=[self.css_file])











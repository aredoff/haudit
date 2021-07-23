import paramiko

class SSHUtil(object):
    def __init__(self, hostname, username, password, port=22):
        self.ip = hostname
        self.port = port
        self.username = username
        self.password = password
        self._login(hostname, username, password, port)

    def _login(self, hostname, username, password, port=22):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=hostname, port=port, username=username, password=password)

    def execute_command(self, command_str):
        input, output, err = self.ssh.exec_command(command_str)
        resp, error = output.read(), err.read()
        if resp:
            return resp.decode("utf8", "ignore")
        else:
            return None

    def upload_file(self, local_file_path, remote_file_path):
        sftp = self.ssh.open_sftp()
        sftp.put(local_file_path, remote_file_path)
        sftp.close()

    def download_file(self, remote_file_path, local_file_path):
        sftp = self.ssh.open_sftp()
        sftp.get(remote_file_path, local_file_path)
        sftp.close()
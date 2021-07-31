from audit import Audit
from ssh import SSHUtil
import argparse
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Audit linux systems')
    parser.add_argument('-s', '--server', required=True, type=str, help='Hostname or ip address')
    parser.add_argument('-u', '--user', type=str, default='root', help='SSH Username, root - default')
    parser.add_argument('-p', '--password', type=str, default=None, help='SSH Password? default - None')
    parser.add_argument('-k', '--key', type=str, default=None, help='Path to ssh private key, default = None')
    parser.add_argument('--pdf', type=str, default=None, help='Path to pdf report file')

    args = parser.parse_args()

    os.environ["SERVER_ADDRESS"] = args.server

    ssh_client = SSHUtil(hostname=args.server, username=args.user, password=args.password, key_filename=args.key)
    a = Audit(ssh_client=ssh_client)
    report = a.execute_queries()
    if args.pdf:
        a.printPdfReport(report, args.pdf)
    else:
        a.printReport(report)


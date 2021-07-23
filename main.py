from audit import Audit
from dotenv import load_dotenv
import os

load_dotenv()
ssh_user = os.getenv('SSH_USER')
ssh_password = os.getenv('SSH_PASSWORD')
test_hostname = os.getenv('TEST_HOSTNAME')

a = Audit(hostname=test_hostname, username=ssh_user, password=ssh_password)
report = a.execute_queries()
a.printReport(report)

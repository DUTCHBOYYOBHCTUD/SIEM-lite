import re
import sqlite3
from datetime import datetime

# Path to your log file
LOG_FILE = 'logs/sample_ssh.log'

# Connect to SQLite (it will create the file if it doesn't exist)
conn = sqlite3.connect('database/siem.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS ssh_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    ip_address TEXT,
    username TEXT,
    action TEXT
)
''')

# Sample log line:
# Jan 26 10:23:01 myserver sshd[19999]: Failed password for root from 192.168.1.10 port 22 ssh2
log_pattern = re.compile(
    r'^(?P<month>\w{3}) (?P<day>\d{1,2}) (?P<time>\d{2}:\d{2}:\d{2}) .*sshd.*: (?P<action>Failed|Accepted) password for (?P<username>\w+) from (?P<ip>[\d.]+)'
)

# Convert syslog timestamp to ISO format
def parse_timestamp(month, day, time):
    current_year = datetime.now().year
    log_time_str = f"{month} {day} {current_year} {time}"
    return datetime.strptime(log_time_str, "%b %d %Y %H:%M:%S").isoformat()

def parse_logs():
    with open(LOG_FILE, 'r') as file:
        for line in file:
            match = log_pattern.match(line)
            if match:
                data = match.groupdict()
                timestamp = parse_timestamp(data['month'], data['day'], data['time'])
                ip_address = data['ip']
                username = data['username']
                action = data['action']

                cursor.execute('''
                    INSERT INTO ssh_logs (timestamp, ip_address, username, action)
                    VALUES (?, ?, ?, ?)
                ''', (timestamp, ip_address, username, action))
    
    conn.commit()
    print("Logs parsed and stored successfully.")

if __name__ == '__main__':
    parse_logs()
    conn.close()

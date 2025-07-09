import sqlite3
from datetime import datetime, timedelta, time
import os

# Ensure alerts directory exists
os.makedirs('database', exist_ok=True)

# Connect to the logs database
conn = sqlite3.connect('database/siem.db')
cursor = conn.cursor()

# Create table for alerts if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    ip_address TEXT,
    alert_type TEXT,
    severity TEXT,
    description TEXT
)
''')

def detect_brute_force(time_window_minutes=5, threshold=3):
    cursor.execute('SELECT timestamp, ip_address FROM ssh_logs WHERE action="Failed" ORDER BY timestamp')
    rows = cursor.fetchall()

    failed_attempts = {}
    for timestamp_str, ip in rows:
        timestamp = datetime.fromisoformat(timestamp_str)
        failed_attempts.setdefault(ip, []).append(timestamp)

    for ip, timestamps in failed_attempts.items():
        for i in range(len(timestamps)):
            window = [t for t in timestamps if 0 <= (t - timestamps[i]).total_seconds() <= time_window_minutes * 60]
            if len(window) >= threshold:
                description = f"{len(window)} failed login attempts from IP {ip} within {time_window_minutes} minutes."
                cursor.execute('''
                    INSERT INTO alerts (timestamp, ip_address, alert_type, severity, description)
                    VALUES (?, ?, ?, ?, ?)
                ''', (datetime.now().isoformat(), ip, 'Brute Force Attempt', 'High', description))
                break

    conn.commit()
    print("Brute force detection complete.")

def detect_login_from_new_ip():
    cursor.execute('SELECT timestamp, ip_address, username FROM ssh_logs WHERE action="Accepted" ORDER BY timestamp')
    rows = cursor.fetchall()

    known_ips = {}

    for timestamp_str, ip, user in rows:
        if user not in known_ips:
            known_ips[user] = set()
            known_ips[user].add(ip)
        else:
            if ip not in known_ips[user]:
                description = f"User '{user}' logged in from new IP address {ip}."
                cursor.execute('''
                    INSERT INTO alerts (timestamp, ip_address, alert_type, severity, description)
                    VALUES (?, ?, ?, ?, ?)
                ''', (timestamp_str, ip, 'Login from New IP', 'Medium', description))
                known_ips[user].add(ip)

    conn.commit()
    print("Login from new IP detection complete.")

def detect_failed_then_success(time_window_minutes=10):
    cursor.execute('SELECT timestamp, ip_address, username, action FROM ssh_logs ORDER BY timestamp')
    rows = cursor.fetchall()

    # Create a dict user -> list of (timestamp, action)
    user_logs = {}
    for timestamp_str, ip, user, action in rows:
        timestamp = datetime.fromisoformat(timestamp_str)
        user_logs.setdefault(user, []).append((timestamp, action, ip))

    for user, logs in user_logs.items():
        for i in range(len(logs)):
            if logs[i][1] == "Accepted":
                # Look back for failed attempts in the last X minutes before this success
                success_time = logs[i][0]
                failed_attempts = [log for log in logs[:i] if log[1] == "Failed" and 0 <= (success_time - log[0]).total_seconds() <= time_window_minutes * 60]
                if len(failed_attempts) >= 2:
                    description = (f"User '{user}' had {len(failed_attempts)} failed login attempts "
                                   f"followed by a successful login within {time_window_minutes} minutes.")
                    cursor.execute('''
                        INSERT INTO alerts (timestamp, ip_address, alert_type, severity, description)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (success_time.isoformat(), logs[i][2], 'Failed then Success Login', 'High', description))

    conn.commit()
    print("Failed then success login detection complete.")

def detect_login_outside_business_hours(start_hour=9, end_hour=18):
    cursor.execute('SELECT timestamp, ip_address, username, action FROM ssh_logs WHERE action="Accepted" ORDER BY timestamp')
    rows = cursor.fetchall()

    for timestamp_str, ip, user, action in rows:
        timestamp = datetime.fromisoformat(timestamp_str)
        login_time = timestamp.time()
        if login_time < time(start_hour) or login_time > time(end_hour):
            description = f"User '{user}' logged in outside business hours at {timestamp_str}."
            cursor.execute('''
                INSERT INTO alerts (timestamp, ip_address, alert_type, severity, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp_str, ip, 'Login Outside Business Hours', 'Medium', description))

    conn.commit()
    print("Login outside business hours detection complete.")

if __name__ == '__main__':
    detect_brute_force()
    detect_login_from_new_ip()
    detect_failed_then_success()
    detect_login_outside_business_hours()
    conn.close()

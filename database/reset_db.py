import sqlite3

conn = sqlite3.connect('database/siem.db')
cursor = conn.cursor()

# Delete all rows from tables
cursor.execute("DELETE FROM ssh_logs")
cursor.execute("DELETE FROM alerts")
conn.commit()

print("✅ All log and alert data cleared.")

conn.close()

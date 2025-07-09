# 🔐 SIEM-lite

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Enabled-brightgreen?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/github/license/DUTCHBOYYOBHCTUD/SIEM-lite?color=blue)](LICENSE)
[![Issues](https://img.shields.io/github/issues/DUTCHBOYYOBHCTUD/SIEM-lite)](https://github.com/DUTCHBOYYOBHCTUD/SIEM-lite/issues)
[![Last Commit](https://img.shields.io/github/last-commit/DUTCHBOYYOBHCTUD/SIEM-lite)](https://github.com/DUTCHBOYYOBHCTUD/SIEM-lite)

---

## 📖 Description:

**SIEM-lite** is a lightweight, modular **Security Information and Event Management (SIEM)** tool built in Python. It parses and analyzes logs (e.g., SSH logs) to detect potential security threats such as:
- Brute-force login attempts
- Logins from new IPs
- Failed-then-success login sequences
- Logins outside business hours

Includes a **Streamlit-powered dashboard** for real-time viewing and status updates.

---

## 📁 Project Structure:

SIEM-lite/
├── dashboard/ # Streamlit dashboard
│ └── app.py
├── database/ # SQLite setup and reset script
│ └── reset_db.py
├── detector/ # Detection logic
│ └── detector.py
├── logs/ # Sample log files
│ ├── test_ssh.log
│ └── sample_ssh.log
├── parser/ # Log parser
│ └── ssh_log_parser.py
├── utils/ # (Optional) Utility functions
├── run_siem.py # Master automation script
├── README.md
└── LICENSE
---

## ⚙️ Setup Instructions

### ✅ 1. Clone the Repository:
git clone https://github.com/DUTCHBOYYOBHCTUD/SIEM-lite.git
cd SIEM-lite

### ✅ 2. Create and Activate Virtual Environment: 
bash
Copy
Edit
python -m venv .venv
.\.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # Mac/Linux

### ✅ 3. Install Dependencies:
pip install -r requirements.txt
If requirements.txt doesn't exist, manually install:
pip install streamlit pandas

### 🚀 How to Run:
# 🛠 Run the Master Script
python run_siem.py
This will:
Generate or use a log file
Run the parser
Perform security detections
Ask if you'd like to launch the dashboard

### 📊 Launch the Dashboard Only:
cd dashboard
streamlit run app.py

### 🔍 Detection Features:
✅ Brute force detection
✅ Login from unknown IPs
✅ Failed login followed by success
✅ Login during off-hours

## 🧪 Sample Log Format:
The logs are expected to resemble SSH login attempts, similar to:
Jul  9 14:05:30 server sshd[12345]: Failed password for invalid user admin from 192.168.0.1 port 22 ssh2
Jul  9 14:05:40 server sshd[12345]: Accepted password for root from 10.0.0.2 port 22 ssh2

### 📦 Future Improvements:
Add support for HTTP, FTP, or firewall logs
Email alerts for suspicious behavior
Role-based access to dashboard
Log ingestion from external devices (IoT, sensors)

## 🤝 Contributing:
Pull requests are welcome! Please open an issue first to discuss what you would like to change.

## 📄 License:
This project is licensed under the MIT License — see the LICENSE file for details.

## 👨‍💻 Developed By:
✨ Chris Kuriakose..aka...Empuraan





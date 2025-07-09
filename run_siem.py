import subprocess
import os
import time

LOG_FILE = "logs/test_ssh.log"
PARSED_LOG_FILE = "parsed_logs.json"

def banner(msg):
    print("\n" + "=" * 60)
    print(msg)
    print("=" * 60)

def check_log_file():
    if not os.path.exists(LOG_FILE):
        banner("[+] Creating sample log file: " + LOG_FILE)
        with open(LOG_FILE, "w") as f:
            f.write("Jul  9 14:33:21 localhost sshd[12345]: Failed password for root from 192.168.0.100 port 22 ssh2\n")
    else:
        banner("[+] Using existing log file: " + LOG_FILE)

def run_parser():
    banner("[1] Running Parser")
    result = subprocess.run(
        ["python", "parser/ssh_log_parser.py", LOG_FILE],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("[!] Parser Error:", result.stderr)

def run_detector():
    banner("[2] Running Detector")
    result = subprocess.run(
        ["python", "detector/detector.py", PARSED_LOG_FILE],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("[!] Detector Error:", result.stderr)

def run_dashboard():
    banner("[3] Starting Dashboard (optional)")
    print("Launching dashboard in a separate terminal...\n")
    time.sleep(2)

    venv_python = os.path.join(".venv", "Scripts", "python.exe")

    if not os.path.exists(venv_python):
        print("[!] .venv Python executable not found.")
        return

    subprocess.Popen([venv_python, "-m", "streamlit", "run", "dashboard/app.py"])
    print("[+] Dashboard launched (using .venv environment)")


def main():
    banner("SIEM-LITE MASTER RUN SCRIPT")
    check_log_file()
    run_parser()
    run_detector()
    user_input = input("\nDo you want to launch the dashboard? (y/n): ")
    if user_input.lower() == "y":
        run_dashboard()
    else:
        print("All components tested. Exiting.")

if __name__ == "__main__":
    main()

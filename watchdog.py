import os
import subprocess
import socket
from datetime import datetime
import platform

LOG_FILE = "watchdog_log.txt"
PING_TARGET = "google.com"
DNS_TARGET = "nitrkl.ac.in"
PING_COUNT = "5"

def get_ping_flag():
    plat = platform.system().lower()
    if "windows" in plat:
        return "-n"
    return "-c" 

def ping_target(target):
    ping_flag = get_ping_flag()
    cmd = ["ping", ping_flag, PING_COUNT, target]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return res.stdout
    except Exception as e:
        return f"Ping error: {e}"

def resolve_dns(name):
    try:
        ip = socket.gethostbyname(name)
        return ip
    except Exception as e:
        return f"DNS resolution failed: {e}"

def log_block(ping_out, dns_ip):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"\n======= WATCHDOG LOG =======\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        f.write("PING OUTPUT:\n")
        f.write(ping_out + "\n")
        f.write("DNS RESOLUTION:\n")
        f.write(f"{DNS_TARGET} -> {dns_ip}\n")

if __name__ == "__main__":
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[*] Network Watchdog Initiated... {ts}")

    ping_out = ping_target(PING_TARGET)
    dns_ip = resolve_dns(DNS_TARGET)

    log_block(ping_out, dns_ip)
    print("[+] Logged results to", LOG_FILE)
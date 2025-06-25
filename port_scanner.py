import socket
import threading
import tkinter as tk
from tkinter import messagebox
import datetime

# === Global variables ===
log_filename = "scan_results.txt"

# === Function to log results to file ===
def log_to_file(text):
    with open(log_filename, "a") as f:
        f.write(text + "\n")

# === TCP port scan function ===
def scan_tcp_port(ip, port, results_box):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        if result == 0:
            result_text = f"[+] TCP Port {port} is OPEN"
            results_box.insert(tk.END, result_text + "\n")
            log_to_file(result_text)
        s.close()
    except:
        pass

# === UDP port scan function ===
def scan_udp_port(ip, port, results_box):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.sendto(b'', (ip, port))
        try:
            s.recvfrom(1024)
            result_text = f"[+] UDP Port {port} is OPEN"
        except socket.timeout:
            result_text = f"[+] UDP Port {port} is OPEN (or filtered)"
        results_box.insert(tk.END, result_text + "\n")
        log_to_file(result_text)
        s.close()
    except:
        pass

# === Main scanning logic (runs in thread) ===
def start_scan(ip, start_port, end_port, protocol, results_box):
    results_box.insert(tk.END, f"Scan started at {datetime.datetime.now()}\n")
    log_to_file(f"=== Scan Started: {datetime.datetime.now()} ===")
    log_to_file(f"Target: {ip}, Ports: {start_port}-{end_port}, Protocol: {protocol}\n")

    for port in range(start_port, end_port + 1):
        if protocol == "TCP":
            scan_tcp_port(ip, port, results_box)
        else:
            scan_udp_port(ip, port, results_box)

    results_box.insert(tk.END, "\n[✓] Scan complete.\n")
    log_to_file("[✓] Scan complete.\n")

# === Triggered when "Start Scan" is clicked ===
def trigger_scan():
    ip = ip_entry.get()
    try:
        start = int(start_port.get())
        end = int(end_port.get())
        protocol = scan_type.get()

        results.delete(1.0, tk.END)
        threading.Thread(target=start_scan, args=(ip, start, end, protocol, results)).start()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid port numbers.")

# === GUI Setup ===
root = tk.Tk()
root.title("Advanced Python Port Scanner")
root.geometry("600x500")

# IP Address Input
tk.Label(root, text="Target IP:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
ip_entry = tk.Entry(root, width=30)
ip_entry.grid(row=0, column=1, pady=5)

# Start Port Input
tk.Label(root, text="Start Port:").grid(row=1, column=0, sticky='w', padx=10)
start_port = tk.Entry(root, width=10)
start_port.grid(row=1, column=1, sticky='w')

# End Port Input
tk.Label(root, text="End Port:").grid(row=2, column=0, sticky='w', padx=10)
end_port = tk.Entry(root, width=10)
end_port.grid(row=2, column=1, sticky='w')

# Protocol Selection
scan_type = tk.StringVar(value="TCP")
tk.Radiobutton(root, text="TCP", variable=scan_type, value="TCP").grid(row=3, column=0, sticky='w', padx=10)
tk.Radiobutton(root, text="UDP", variable=scan_type, value="UDP").grid(row=3, column=1, sticky='w')

# Start Button
tk.Button(root, text="Start Scan", command=trigger_scan, bg="green", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

# Results Text Box
results = tk.Text(root, width=72, height=20)
results.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

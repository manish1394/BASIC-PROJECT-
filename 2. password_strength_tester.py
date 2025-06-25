import re
import tkinter as tk
from tkinter import messagebox
from random import choice, randint
import string

# Common weak passwords
common_passwords = [
    '123456', 'password', 'qwerty', '123456789', '12345',
    '12345678', '111111', '123123', 'abc123', 'password1'
]

# Password strength checker
def check_strength(password):
    strength_score = 0
    suggestions = []

    if len(password) >= 8:
        strength_score += 1
    else:
        suggestions.append("• Use at least 8 characters.")

    if re.search(r'\d', password):
        strength_score += 1
    else:
        suggestions.append("• Include at least one number.")

    if re.search(r'[A-Z]', password):
        strength_score += 1
    else:
        suggestions.append("• Include at least one uppercase letter.")

    if re.search(r'[a-z]', password):
        strength_score += 1
    else:
        suggestions.append("• Include at least one lowercase letter.")

    if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        strength_score += 1
    else:
        suggestions.append("• Include at least one special character.")

    if password.lower() in common_passwords:
        strength_score = 0
        suggestions = ["• This password is too common. Avoid using it."]

    return strength_score, suggestions

# Random strong password generator
def generate_strong_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(choice(chars) for _ in range(randint(12, 16)))

# Button click handler
def evaluate_password():
    password = entry.get()
    score, tips = check_strength(password)

    if score >= 4:
        result = "✅ Strong Password"
        color = "#4CAF50"
    elif score == 3:
        result = "⚠️ Moderate Password"
        color = "#FF9800"
    else:
        result = "❌ Weak Password"
        color = "#F44336"

    suggestion_text = "\n".join(tips)
    strong_pass = generate_strong_password()
    result_label.config(text=result, fg=color)
    suggestion_label.config(text=f"{suggestion_text}\n\n💡 Suggested Strong Password:\n{strong_pass}")

# GUI Setup
root = tk.Tk()
root.title("🔐 AI-Powered Password Strength Tester")
root.geometry("500x400")
root.config(bg="#f7f9fc")
root.resizable(False, False)

# Title
tk.Label(root, text="Password Strength Checker", font=("Helvetica", 18, "bold"), bg="#f7f9fc", fg="#333").pack(pady=20)

# Entry
entry_frame = tk.Frame(root, bg="#f7f9fc")
entry_frame.pack(pady=5)
tk.Label(entry_frame, text="🔑 Enter Password:", font=("Helvetica", 12), bg="#f7f9fc").pack(side="left", padx=5)
entry = tk.Entry(entry_frame, show="*", width=30, font=("Helvetica", 12))
entry.pack(side="left", padx=5)

# Check Button
tk.Button(root, text="Check Strength", command=evaluate_password,
          font=("Helvetica", 12), bg="#007BFF", fg="white", width=20, height=1).pack(pady=15)

# Result Label
result_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"), bg="#f7f9fc")
result_label.pack(pady=5)

# Suggestions
suggestion_label = tk.Label(root, text="", font=("Helvetica", 11), bg="#f7f9fc", fg="#555", justify="left")
suggestion_label.pack(pady=10)

# Footer Tip
tk.Label(root, text="Tips: Use a mix of UPPER/lowercase, numbers, and symbols.",
         font=("Helvetica", 9), bg="#f7f9fc", fg="gray").pack(side="bottom", pady=10)

root.mainloop()


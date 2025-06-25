import wave
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# === Utility Functions ===
def text_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)

# === Image Steganography ===
def hide_text_in_image(input_path, output_path, message):
    image = Image.open(input_path)
    binary_message = text_to_binary(message) + '1111111111111110'

    if image.mode != 'RGB':
        raise ValueError("Image mode must be RGB")

    pixels = list(image.getdata())
    new_pixels = []
    binary_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if binary_index < len(binary_message):
            r = (r & ~1) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            g = (g & ~1) | int(binary_message[binary_index])
            binary_index += 1
        if binary_index < len(binary_message):
            b = (b & ~1) | int(binary_message[binary_index])
            binary_index += 1
        new_pixels.append((r, g, b))

    image.putdata(new_pixels)
    image.save(output_path)
    return "Message hidden in image."

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    binary_data = ''
    for pixel in image.getdata():
        for color in pixel:
            binary_data += str(color & 1)
    end_index = binary_data.find('1111111111111110')
    if end_index != -1:
        return binary_to_text(binary_data[:end_index])
    return "No hidden message found."

# === Audio Steganography ===
def hide_text_in_audio(input_path, output_path, message):
    audio = wave.open(input_path, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    message_binary = text_to_binary(message) + '1111111111111110'

    if len(message_binary) > len(frame_bytes):
        raise ValueError("Message too long for audio file.")

    for i in range(len(message_binary)):
        frame_bytes[i] = (frame_bytes[i] & 254) | int(message_binary[i])

    modified_audio = wave.open(output_path, 'wb')
    modified_audio.setparams(audio.getparams())
    modified_audio.writeframes(bytes(frame_bytes))
    modified_audio.close()
    audio.close()
    return "Message hidden in audio."

def extract_text_from_audio(audio_path):
    audio = wave.open(audio_path, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()
    extracted_bits = [str(byte & 1) for byte in frame_bytes]
    binary_data = ''.join(extracted_bits)
    end_index = binary_data.find('1111111111111110')
    if end_index != -1:
        return binary_to_text(binary_data[:end_index])
    return "No hidden message found."

# === GUI ===
def browse_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def save_file(entry):
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def process_action():
    in_file = input_file.get()
    out_file = output_file.get()
    secret = message_entry.get()
    try:
        if method.get() == "Image - Hide":
            result = hide_text_in_image(in_file, out_file, secret)
        elif method.get() == "Image - Extract":
            result = extract_text_from_image(in_file)
        elif method.get() == "Audio - Hide":
            result = hide_text_in_audio(in_file, out_file, secret)
        elif method.get() == "Audio - Extract":
            result = extract_text_from_audio(in_file)
        else:
            result = "Invalid option."
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# === GUI Setup ===
root = tk.Tk()
root.title("Advanced Steganography Tool")
root.geometry("600x450")

# Input & Output
tk.Label(root, text="Input File:").grid(row=0, column=0, sticky='e')
input_file = tk.Entry(root, width=40)
input_file.grid(row=0, column=1)
tk.Button(root, text="Browse", command=lambda: browse_file(input_file)).grid(row=0, column=2)

tk.Label(root, text="Output File:").grid(row=1, column=0, sticky='e')
output_file = tk.Entry(root, width=40)
output_file.grid(row=1, column=1)
tk.Button(root, text="Save As", command=lambda: save_file(output_file)).grid(row=1, column=2)

# Message
tk.Label(root, text="Secret Message:").grid(row=2, column=0, sticky='e')
message_entry = tk.Entry(root, width=40)
message_entry.grid(row=2, column=1, columnspan=2)

# Method Options
method = tk.StringVar(value="Image - Hide")
options = ["Image - Hide", "Image - Extract", "Audio - Hide", "Audio - Extract"]
tk.Label(root, text="Action:").grid(row=3, column=0, sticky='e')
tk.OptionMenu(root, method, *options).grid(row=3, column=1, sticky='w')

# Action Button
tk.Button(root, text="Run", bg="green", fg="white", command=process_action).grid(row=4, column=1, pady=10)

# Result Output
tk.Label(root, text="Result / Extracted Message:").grid(row=5, column=0, columnspan=3)
result_box = tk.Text(root, height=10, width=70)
result_box.grid(row=6, column=0, columnspan=3, padx=10)

root.mainloop()

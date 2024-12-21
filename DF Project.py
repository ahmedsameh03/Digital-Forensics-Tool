import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import ctypes


def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)


def clear_output():
    text_output.delete(1.0, tk.END)


def collect_network_data():
    clear_output()
    output = run_command("netstat -an")
    text_output.insert(tk.END, "=== Network Forensics (netstat) ===\n", "header")
    text_output.insert(tk.END, output + "\n")


def analyze_disk():
    clear_output()
    folder_path = filedialog.askdirectory(title="Select a Disk or Folder to Analyze")
    if folder_path:
        output = run_command(f"dir \"{folder_path}\" /T:C /T:W /T:A /S")
        text_output.insert(tk.END, f"=== Disk Forensics: Analysis of {folder_path} ===\n", "header")
        text_output.insert(tk.END, output + "\n")
    else:
        text_output.insert(tk.END, "No folder selected for disk analysis.\n")


def collect_memory_data():
    clear_output()
    output = run_command("tasklist")
    text_output.insert(tk.END, "=== Memory Forensics (tasklist) ===\n", "header")
    text_output.insert(tk.END, output + "\n")


def collect_registry_data():
    clear_output()
    output = run_command("reg query HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run")
    text_output.insert(tk.END, "=== Windows Registry Forensics (Autostart Programs) ===\n", "header")
    text_output.insert(tk.END, output + "\n")


def collect_persistence_mechanisms():
    """Collect persistence mechanisms in Windows by checking the registry for startup entries."""
    clear_output()
    output = run_command("reg query HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run")
    text_output.insert(tk.END, "=== Persistence Mechanisms (Startup Programs) ===\n", "header")
    text_output.insert(tk.END, output + "\n")


def collect_malware_analysis():
    clear_output()
    file_path = filedialog.askopenfilename(title="Select a File to Scan for Malware")
    if file_path:
        output = f"Scanning the file: {file_path}\n"
        if os.path.exists(file_path):
            output += f"File found: {file_path}\nMalware scan result: No threats found (simulated).\n"
        else:
            output += f"File not found: {file_path}\n"
        text_output.insert(tk.END, "=== Malware Analysis ===\n", "header")
        text_output.insert(tk.END, output + "\n")
    else:
        text_output.insert(tk.END, "No file selected for malware analysis.\n")


def create_gui():
    app = tk.Tk()
    app.title("Digital Forensics Tool")
    app.geometry("800x600")
    app.config(bg="#34495E") 

    frame = tk.Frame(app, bg="#34495E")
    frame.pack(pady=10)

    button_style = {"relief": "flat", "width": 25, "height": 2, "font": ("Arial", 10, "bold"), "bg": "#2ECC71", "fg": "#FFFFFF", "bd": 0, "cursor": "hand2"}
    
    tk.Button(frame, text="Network Forensics", command=collect_network_data, **button_style).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(frame, text="Disk Forensics", command=analyze_disk, **button_style).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(frame, text="Memory Forensics", command=collect_memory_data, **button_style).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(frame, text="Persistence Mechanisms", command=collect_persistence_mechanisms, **button_style).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(frame, text="Malware Analysis", command=collect_malware_analysis, **button_style).grid(row=1, column=2, padx=5, pady=5)


    button_style_red = {"relief": "flat", "width": 18, "height": 2, "font": ("Arial", 10, "bold"), "bg": "#E74C3C", "fg": "#FFFFFF", "bd": 0, "cursor": "hand2"}


    tk.Button(frame, text="Clear Output", command=clear_output, **button_style_red).grid(row=1, column=1, padx=5, pady=5)


    global text_output
    text_output = ScrolledText(app, wrap=tk.WORD, height=20, font=("Courier", 10), bg="#2C3E50", fg="white", insertbackground="white")
    text_output.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    text_output.tag_config("header", font=("Arial", 12, "bold"), foreground="#F39C12")

    app.mainloop()


try:
    create_gui()
except Exception as e:
    print(f"Error starting the program: {e}")
    exit(1)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from components.encrypt import encrypt_folder
from components.decrypt import decrypt_folder
import os
import logging

# Configurez le logging
logging.basicConfig(filename='activity_log.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

app = tk.Tk()
app.title("CryptoFolder")
app.geometry('500x700')
app.config(bg='black')

style = ttk.Style(app)
style.theme_use('clam')  # Utilisez un thème qui permet la personnalisation

# Style pour les boutons
style.configure('TButton', background='black', foreground='lime green', borderwidth=1, focusthickness=3, focuscolor='none')
style.map('TButton', background=[('active', 'green'), ('pressed', 'lime green')])

# Style pour les entrées
style.configure('TEntry', foreground='lime green', background='black', borderwidth=1)
style.map('TEntry', fieldbackground=[('!disabled', 'black')], foreground=[('!disabled', 'lime green')])

# Définition des variables globales
folder_path = tk.StringVar(app)
password = tk.StringVar(app)

def export_log():
    export_path = filedialog.asksaveasfilename(defaultextension='.log',
                                               filetypes=[("Log files", "*.log"), ("All files", "*.*")])
    if export_path:
        with open('activity_log.log', 'r') as log_file:
            with open(export_path, 'w') as export_file:
                export_file.write(log_file.read())
        messagebox.showinfo("Export Successful", "The log has been exported successfully.")

log_display = ScrolledText(app, height=10)
log_display.pack(pady=10, padx=10, fill='both', expand=True)

def update_log_display():
    with open('activity_log.log', 'r') as log_file:
        log_display.delete('1.0', tk.END)
        log_display.insert(tk.END, log_file.read())

def select_folder():
    path = filedialog.askdirectory()
    folder_path.set(path)
    if path:
        display_folder_structure(path)


def display_folder_structure(path):
    structure = ""
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        structure += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            structure += f"{subindent}{f}\n"
    text_area.config(state=tk.NORMAL)
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, structure)
    text_area.config(state=tk.DISABLED)

app_directory = os.path.dirname(os.path.realpath(__file__))  # Obtenez le chemin du répertoire où se trouve app.py

def encrypt():
    if folder_path.get() and password.get():
        encrypt_folder(folder_path.get(), password.get(), app_directory)
        status_label.config(text="Chiffrement réussi!", fg="lime green")
    else:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un dossier et entrer une phrase secrète!")

def decrypt():
    if folder_path.get() and password.get():
        decrypt_folder(folder_path.get(), password.get(), app_directory)
        status_label.config(text="Déchiffrement réussi!", fg="lime green")
    else:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un dossier et entrer une phrase secrète!")

# Widgets et layout
tk.Label(app, text="Chemin du dossier:", bg='black', fg='lime green').pack()
entry = ttk.Entry(app, textvariable=folder_path, width=50, style='TEntry')
entry.pack(pady=10)

tk.Label(app, text="Clé secrète:", bg='black', fg='lime green').pack()
pass_entry = ttk.Entry(app, textvariable=password, show='*', width=50, style='TEntry')
pass_entry.pack(pady=10)

ttk.Button(app, text="Parcourir", command=select_folder, style='TButton').pack()

text_area = ScrolledText(app, wrap=tk.WORD, width=60, height=10, bg='black', fg='lime green')
text_area.pack(pady=10, padx=10)
text_area.config(state=tk.DISABLED)

ttk.Button(app, text="Chiffrer", command=encrypt, style='TButton').pack(pady=5)
ttk.Button(app, text="Déchiffrer", command=decrypt, style='TButton').pack(pady=5)
ttk.Button(app, text="Refresh Log", command=update_log_display, style='TButton').pack(pady=5)
ttk.Button(app, text="Export Log", command=export_log, style='TButton').pack(pady=5)

status_label = tk.Label(app, text="", bg='black', fg='lime green')
status_label.pack(pady=10)

app.mainloop()
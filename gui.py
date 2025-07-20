import tkinter as tk
from tkinter import filedialog, messagebox
from backup import BackupManager
import threading

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Backup Logger")

        # Source folder
        tk.Label(root, text="Source folder:").grid(row=0, column=0, sticky="w")
        self.source_entry = tk.Entry(root, width=50)
        self.source_entry.grid(row=0, column=1, padx=5)
        tk.Button(root, text="Browse", command=self.select_source).grid(row=0, column=2)

        # Destination folder
        tk.Label(root, text="Destination folder:").grid(row=1, column=0, sticky="w")
        self.dest_entry = tk.Entry(root, width=50)
        self.dest_entry.grid(row=1, column=1, padx=5)
        tk.Button(root, text="Browse", command=self.select_dest).grid(row=1, column=2)

        # Compression checkbox
        self.compress_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Compress to ZIP", variable=self.compress_var).grid(row=2, column=1, sticky="w")

        # Backup button
        self.backup_button = tk.Button(root, text="Start Backup", command=self.run_backup)
        self.backup_button.grid(row=3, column=1, pady=10)

        # Status label
        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.grid(row=4, column=0, columnspan=3)

    def select_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, folder)

    def select_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, folder)

    def run_backup(self):
        source = self.source_entry.get()
        destination = self.dest_entry.get()
        compress = self.compress_var.get()

        if not source or not destination:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return

        # Disable button to avoid multiple clicks
        self.backup_button.config(state=tk.DISABLED)
        self.status_label.config(text="Backup in progress...")

        # Run backup in a thread to avoid freezing GUI
        thread = threading.Thread(target=self.backup_thread, args=(source, destination, compress))
        thread.start()

    def backup_thread(self, source, destination, compress):
        try:
            manager = BackupManager(source, destination)
            backup_path, file_count, duration = manager.perform_backup(compress=compress)
            msg = f"Backup successful at: {backup_path}\nFiles copied: {file_count}\nDuration: {duration:.2f} seconds"
            self.status_label.config(text=msg)
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")
        finally:
            self.backup_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()

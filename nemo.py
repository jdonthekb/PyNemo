import os
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread

def browse_directory():
    folder_selected = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, folder_selected)

def process_files():
    process_button.config(text="Processing...", state=tk.DISABLED)
    directory = directory_entry.get()
    search_str = search_entry.get()
    replace_str = replace_entry.get()
    extension = extension_entry.get()
    ignore_extension = ignore_extension_var.get()

    if not directory or not search_str or not replace_str:
        messagebox.showerror("Error", "All fields except extension are required")
        process_button.config(text="Process", state=tk.NORMAL)
        return

    def process():
        for file in os.listdir(directory):
            if ignore_extension or file.endswith(f".{extension}"):
                file_path = os.path.join(directory, file)
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_contents = file.read()
                
                file_contents = file_contents.replace(search_str, replace_str)

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(file_contents)
        
        root.after(0, post_process)

    def post_process():
        process_button.config(text="Process", state=tk.NORMAL)
        messagebox.showinfo("Success", "Processing complete")

    Thread(target=process).start()

# Setting up the main window
root = tk.Tk()
root.title("Nemo v1.1 by Joshua Dwight")

# Directory selection
tk.Label(root, text="Directory:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
directory_entry = tk.Entry(root, width=50)
directory_entry.grid(row=0, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", height=2, width=10, command=browse_directory)
browse_button.grid(row=0, column=2, padx=10, pady=10)

# Search string entry
tk.Label(root, text="Search For:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
search_entry = tk.Entry(root, width=50)
search_entry.grid(row=1, column=1, padx=10, pady=10)

# Replace string entry
tk.Label(root, text="Replace With:").grid(row=2, column=0, padx=10, pady=10, sticky='w')
replace_entry = tk.Entry(root, width=50)
replace_entry.grid(row=2, column=1, padx=10, pady=10)

# File extension entry
tk.Label(root, text="File Extension:").grid(row=3, column=0, padx=10, pady=10, sticky='w')
extension_entry = tk.Entry(root, width=3)
extension_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

# Ignore extension checkbox
ignore_extension_var = tk.BooleanVar()
ignore_extension_checkbox = tk.Checkbutton(root, text="Ignore Extension", variable=ignore_extension_var)
ignore_extension_checkbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='w')

# Process button
process_button = tk.Button(root, text="Process", height=2, width=20, command=process_files)
process_button.grid(row=5, column=1, padx=10, pady=10)

root.mainloop()

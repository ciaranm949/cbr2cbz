import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import os

# Define functions to handle each of the features
def convert_files():
    cbr_folder = filedialog.askdirectory(title="Select Folder Containing CBR Files")
    if not cbr_folder:
        return

    output_dir = filedialog.askdirectory(title="Select Output Folder")
    if not output_dir:
        return

    # Gather options
    uncompressed_cbz = uncompressed_cbz_var.get()
    copy_non_cbz = copy_non_cbz_var.get()
    flat_mode = flat_mode_var.get()
    patterns = patterns_entry.get().split(',') if patterns_entry.get() else []

    # Iterate over all CBR files in the selected folder
    for file in os.listdir(cbr_folder):
        if file.lower().endswith(".cbr"):
            cbr_file_path = os.path.join(cbr_folder, file)

            # Build the command for each file
            command = ["python3", "cbr2cbz.py", cbr_file_path, "--output", output_dir]

            if uncompressed_cbz:
                command.append("--uncompressed")
            if copy_non_cbz:
                command.append("--copy")
            if flat_mode:
                command.append("--flat")
            for pattern in patterns:
                command.extend(["--pattern", pattern])

            try:
                # Run the conversion process for each file
                subprocess.run(command, check=True)
            except Exception as e:
                messagebox.showerror("Error", f"Conversion failed for {file}: {e}")
                return

    messagebox.showinfo("Success", "All files converted successfully!")

# Setup the UI
root = tk.Tk()
root.title("CBR to CBZ Converter (Batch Mode)")

# Uncompressed CBZ option
uncompressed_cbz_var = tk.IntVar()
tk.Checkbutton(root, text="Convert to uncompressed CBZ", variable=uncompressed_cbz_var).pack(anchor=tk.W)

# Copy non-CBZ/CBR files option
copy_non_cbz_var = tk.IntVar()
tk.Checkbutton(root, text="Copy non-CBR/CBZ files", variable=copy_non_cbz_var).pack(anchor=tk.W)

# Flat mode option
flat_mode_var = tk.IntVar()
tk.Checkbutton(root, text="Flat mode (all files in top-level folder)", variable=flat_mode_var).pack(anchor=tk.W)

# Pattern matching option
tk.Label(root, text="Pattern matching (comma-separated):").pack(anchor=tk.W)
patterns_entry = tk.Entry(root)
patterns_entry.pack(fill=tk.X)

# Convert button
tk.Button(root, text="Convert", command=convert_files).pack()

# Run the UI
root.mainloop()

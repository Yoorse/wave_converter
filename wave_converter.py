import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

class WAVConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WAV to 44000 Hz Converter")
        self.geometry("400x200")

        self.input_directory = tk.StringVar()
        self.output_directory = tk.StringVar()

        tk.Label(self, text="Input Directory:").pack(pady=5)
        tk.Entry(self, textvariable=self.input_directory, width=50).pack(pady=5)
        tk.Button(self, text="Browse", command=self.browse_input).pack(pady=5)

        tk.Label(self, text="Output Directory:").pack(pady=5)
        tk.Entry(self, textvariable=self.output_directory, width=50).pack(pady=5)
        tk.Button(self, text="Browse", command=self.browse_output).pack(pady=5)

        tk.Button(self, text="Convert", command=self.convert_files).pack(pady=20)

    def browse_input(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_directory.set(directory)

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory.set(directory)

    def convert_files(self):
        input_directory = self.input_directory.get()
        output_directory = self.output_directory.get()

        if not input_directory or not output_directory:
            messagebox.showerror("Error", "Both input and output directories are required!")
            return

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for file in os.listdir(input_directory):
            if file.endswith(".wav"):
                input_path = os.path.join(input_directory, file)
                output_path = os.path.join(output_directory, file)
                subprocess.run(["ffmpeg", "-i", input_path, "-ar", "44000", output_path])

        messagebox.showinfo("Success", "Conversion completed successfully!")

if __name__ == "__main__":
    app = WAVConverterApp()
    app.mainloop()

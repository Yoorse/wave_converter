import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import subprocess

class WAVConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MPC 2000 xl - Audio to 44100 Hz Converter")
        self.geometry("800x600")
        
        self.input_directory = tk.StringVar()
        self.output_directory = tk.StringVar()
        self.use_output_directory = tk.BooleanVar()

        # Load and set background image
        self.background_image = Image.open("source/mpc.jpg")  # Updated to use mpc.jpg
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Styling
        self.button_style = {'bg': 'gray', 'fg': 'white', 'font': ('Courier', 12, 'bold')}
        self.label_style = {'bg': 'black', 'fg': 'white', 'font': ('Courier', 12)}

        # Layout
        self.create_widgets()

    def create_widgets(self):
        # Input Directory
        tk.Label(self, text="Input Directory:", **self.label_style).place(x=50, y=50)
        tk.Entry(self, textvariable=self.input_directory, width=50).place(x=200, y=50)
        tk.Button(self, text="Browse", command=self.browse_input, **self.button_style).place(x=600, y=50)

        # Checkbox for Output Directory
        self.checkbox = tk.Checkbutton(self, text="Use Output Directory (Optional):", variable=self.use_output_directory,
                                       onvalue=True, offvalue=False, command=self.toggle_output_directory, **self.label_style)
        self.checkbox.place(x=50, y=100)

        # Output Directory
        self.output_label = tk.Label(self, text="Output Directory:", **self.label_style)
        self.output_entry = tk.Entry(self, textvariable=self.output_directory, width=50, state=tk.DISABLED)
        self.output_button = tk.Button(self, text="Browse", command=self.browse_output, **self.button_style, state=tk.DISABLED)

        self.output_label.place(x=50, y=150)
        self.output_entry.place(x=200, y=150)
        self.output_button.place(x=600, y=150)

        # Convert Button
        tk.Button(self, text="Convert", command=self.convert_files, **self.button_style).place(x=350, y=200)

        # Status Bar
        self.status = tk.StringVar()
        self.status.set("Ready")
        self.status_bar = tk.Label(self, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.place(x=0, y=580, width=400)  # Set width to 400 to make it narrower

        # Information Textbox
        self.info_text = tk.Text(self, height=10, width=40, bg='black', fg='white', font=('Courier', 12))
        self.info_text.insert(tk.END, "Will create subfolders called Converted, if output folder is not chosen")
        self.info_text.config(state=tk.DISABLED)
        self.info_text.place(x=500, y=300)

    def toggle_output_directory(self):
        if self.use_output_directory.get():
            self.output_entry.config(state=tk.NORMAL)
            self.output_button.config(state=tk.NORMAL)
        else:
            self.output_entry.config(state=tk.DISABLED)
            self.output_button.config(state=tk.DISABLED)

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
        use_output_directory = self.use_output_directory.get()
        output_directory = self.output_directory.get()

        if not input_directory:
            messagebox.showerror("Error", "Input directory is required!")
            return

        if use_output_directory and not output_directory:
            messagebox.showerror("Error", "Output directory is checked but not provided!")
            return

        supported_extensions = (".wav", ".mp3", ".aac", ".flac", ".ogg", ".m4a")

        try:
            for root, _, files in os.walk(input_directory):
                for file in files:
                    if file.lower().endswith(supported_extensions):
                        input_path = os.path.join(root, file)
                        
                        if use_output_directory:
                            output_path = os.path.join(output_directory, os.path.splitext(file)[0] + ".wav")
                        else:
                            converted_folder = os.path.join(root, "converted")
                            if not os.path.exists(converted_folder):
                                os.makedirs(converted_folder)
                            output_path = os.path.join(converted_folder, os.path.splitext(file)[0] + ".wav")
                        
                        # Skip if the file is already converted
                        if os.path.exists(output_path):
                            self.status.set(f"Skipping {file}, already converted.")
                            self.update_idletasks()
                            continue

                        self.status.set(f"Converting {file}...")
                        self.update_idletasks()
                        process = subprocess.Popen(["ffmpeg", "-i", input_path, "-ar", "44100", "-sample_fmt", "s16", output_path],
                                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        for line in process.stderr:
                            self.status.set(line.strip())
                            self.update_idletasks()
                        process.wait()
            self.status.set("Conversion completed successfully!")
            messagebox.showinfo("Success", "Conversion completed successfully!")
        except subprocess.CalledProcessError as e:
            self.status.set("Error occurred during conversion!")
            messagebox.showerror("Error", f"An error occurred during conversion: {e}")
        except Exception as e:
            self.status.set("Unexpected error occurred!")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app = WAVConverterApp()
    app.mainloop()

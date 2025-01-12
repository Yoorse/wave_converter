import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

class WAVConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MPC 2000 xl - Audio to 44000 Hz Converter")
        self.geometry("800x600")
        
        self.input_directory = tk.StringVar()
        self.output_directory = tk.StringVar()

        # Load and set background image
        self.background_image = Image.open("path/to/your/background_image.jpg")  # Update with your image path
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

        # Output Directory
        tk.Label(self, text="Output Directory:", **self.label_style).place(x=50, y=100)
        tk.Entry(self, textvariable=self.output_directory, width=50).place(x=200, y=100)
        tk.Button(self, text="Browse", command=self.browse_output, **self.button_style).place(x=600, y=100)

        # Convert Button
        tk.Button(self, text="Convert", command=self.convert_files, **self.button_style).place(x=350, y=200)

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

        supported_extensions = (".wav", ".mp3", ".aac", ".flac", ".ogg", ".m4a")

        try:
            for file in os.listdir(input_directory):
                if file.lower().endswith(supported_extensions):
                    input_path = os.path.join(input_directory, file)
                    output_path = os.path.join(output_directory, os.path.splitext(file)[0] + ".wav")
                    subprocess.run(["ffmpeg", "-i", input_path, "-ar", "44000", output_path], check=True)
            messagebox.showinfo("Success", "Conversion completed successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred during conversion: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app = WAVConverterApp()
    app.mainloop(

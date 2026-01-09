

import tkinter.filedialog as fd

# Create a file dialog which returns the path of the selected file
def open_file_dialog(filetypes=((".wav Files", "*.wav"),)):
    root = fd.Tk()
    root.withdraw()  # Hide the root window
    file_path = fd.askopenfilename(filetypes=filetypes)
    root.destroy()  # Destroy the root window after use
    return file_path
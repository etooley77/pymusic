

import tkinter.filedialog as fd

# Create a file dialog which returns the path of the selected file
def open_file_dialog(filetypes=((".wav Files", "*.wav"),)):
    # Create a root window and hide it
    root = fd.Tk()
    root.withdraw()

    # Open a file dialog; once the user selects a file or exits, the window is closed
    file_path = fd.askopenfilename(filetypes=filetypes)
    root.destroy()

    return file_path
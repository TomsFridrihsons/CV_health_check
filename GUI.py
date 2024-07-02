import threading
import tkinter as tk
from tkinter import filedialog
from main import FileTarnsfer
import numpy as np
from PIL import Image, ImageTk
import time
import threading


class FolderSelection:

    def __init__(self, root):
        self.mover = FileTarnsfer()
        self.main_frame = None
        self.root = root
        # Setting up window
        self.root.title('Transfer specific dataset classes')
        self.root.geometry('500x300')
        self.root.resizable(True, True)
        self.prev_data_array = np.full((3, 3), None)

    def organize_window(self):
        # Organizing the window
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.upload_frame = tk.Frame(self.main_frame, bg='lightgrey', width=400, height=250)
        self.source_frame = tk.Frame(self.upload_frame, bg='lightblue', width=150, height=200)
        self.destination_frame = tk.Frame(self.upload_frame, bg='lightgreen', width=150, height=200)
        self.upload_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, padx=10, pady=10)
        self.source_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=10, pady=10)
        self.destination_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=10, pady=10)

        self.main_label = tk.Label(self.main_frame, text='Choose a dataset from which you want to transfer data')
        self.main_label.pack(pady=20)

        self.upload_image = Image.open('assets/upload_file.png')
        self.upload_image = self.upload_image.resize((75, 75))
        self.button_image = ImageTk.PhotoImage(self.upload_image)

        self.upload_source_button = tk.Button(self.source_frame, image=self.button_image,
                                              command=self.choose_source_directory_path)
        self.upload_destination_button = tk.Button(self.destination_frame, image=self.button_image,
                                                   command=self.choose_destination_directory_path)
        self.upload_source_button.pack(side=tk.TOP, padx=10, pady=10)
        self.upload_destination_button.pack(side=tk.TOP, padx=10, pady=10)
        self.continue_button = tk.Button(self.main_frame, text='Continue', command=self.start_data_processing)
        self.continue_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    def remove_main_frame(self):
        self.main_frame.destroy()
        del self.main_frame

    def organize_second_screen(self):
        self.second_screen = tk.Frame(self.root, bg='#294E5A')
        self.second_screen.pack(expand=True, fill=tk.BOTH)

        self.top_label = tk.Label(self.second_screen, text='Transferring data...', bg='#294E5A', fg='white')
        self.top_label.grid(row=0, column=0, padx=10, pady=10)

        self.center_information_frame = tk.Frame(self.second_screen, bg='#47889E', width=400, height=150)
        self.center_information_frame.grid(row=1, column=0, padx=10, pady=10)

        label1 = tk.Label(self.center_information_frame, text="Train dataset images", bg='#47889E', fg='white')
        label1.grid(row=0, column=1, padx=5, pady=5)

        label2 = tk.Label(self.center_information_frame, text="Validation dataset images", bg='#47889E', fg='white')
        label2.grid(row=0, column=2, padx=5, pady=5)

        label3 = tk.Label(self.center_information_frame, text="Test dataset images", bg='#47889E', fg='white')
        label3.grid(row=0, column=3, padx=5, pady=5)

        label4 = tk.Label(self.center_information_frame, text="Found files", bg='#47889E', fg='white')
        label4.grid(row=1, column=0, padx=5, pady=5)

        label5 = tk.Label(self.center_information_frame, text="Moved files", bg='#47889E', fg='white')
        label5.grid(row=2, column=0, padx=5, pady=5)

        label6 = tk.Label(self.center_information_frame, text="Lost files", bg='#47889E', fg='white')
        label6.grid(row=3, column=0, padx=5, pady=5)

    def choose_source_directory_path(self):
        self.mover.source_path = filedialog.askdirectory()
        if self.mover.source_path:
            print(f'Selected source directory: {self.mover.source_path}')

    def choose_destination_directory_path(self):
        self.mover.destination_path = filedialog.askdirectory()
        if self.mover.destination_path:
            print(f'Selected source directory: {self.mover.destination_path}')

    def get_source_path(self):
        return self.mover.source_path

    def get_destination_path(self):
        return self.mover.destination_path

    def start_data_processing(self):
        if not self.mover.source_path or not self.mover.destination_path:
            self.main_label.config(text='Please choose both directories to continue transferring data')
            return
        else:
            self.remove_main_frame()
            self.organize_second_screen()
            thread = threading.Thread(target=self.mover.main_code)
            thread.start()
            self.root.after(100, self.display_data)  # Schedule display_data to run periodically
        print("code executed")
        print(self.mover.file_data)

    def main_process(self):
        self.organize_window()

    def display_data(self):
        data_array = self.mover.file_data.reshape(3, 3).T
        not_equal_mask = data_array != self.prev_data_array

        if not_equal_mask.any():
            # Get the indices of elements that are not equal
            indices_not_equal = np.where(not_equal_mask)

            # Update the GUI for the indices where elements are not equal
            for idx in zip(indices_not_equal[0], indices_not_equal[1]):
                if data_array[idx[0], idx[1]] is not None:  # Check if the new value is not None
                    label = tk.Label(self.center_information_frame, text=data_array[idx[0], idx[1]], bg='#47889E',
                                     fg='white')
                    label.grid(row=idx[0] + 1, column=idx[1] + 1, padx=5, pady=5)

            self.prev_data_array = data_array.copy()  # Update the previous data array

        self.root.after(100, self.display_data)  # Reschedule display_data to run again after 100ms


if __name__ == "__main__":
    root = tk.Tk()  # Creating a root window
    app = FolderSelection(root)
    app.organize_window()
    root.mainloop()

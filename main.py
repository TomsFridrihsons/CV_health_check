import os
import shutil
import numpy as np


def none_counter(none_array):
    none_count = -1
    for i in range(len(none_array)):
        if none_array[i] is None:
            none_count += 1
            print(none_count)
    return none_count


class FileTarnsfer:

    def __init__(self):
        # Define the main directory
        self.source_path = None
        # Directory to where you need to move images and labels (modify as needed)
        self.destination_path = None
        # List of main subdirectories to iterate over
        self.folders = ["train", "test", "valid"]
        # List of subdirectories within each main folder
        self.subfolders = ["images", "labels"]
        self.txt_files_with_the_class = []
        self.not_found_files = []
        self.file_data = np.full(9, None)
        self.class_nr = '1'

    def dataset_health(self):
        class_counter = np.zeros(5)
        file_has_class = []
        files_with_class = np.zeros(5)
        os.chdir(self.source_path)
        for filename in os.listdir('.'):
            file_has_class.clear()
            if filename.endswith(".txt"):
                with open(filename, "r") as file:
                    for line in file:
                        class_nr = line[0]
                        class_nr = int(class_nr)
                        class_counter[class_nr] += 1
                        if class_nr not in file_has_class:
                            file_has_class.append(class_nr)
                    file.close()
                for i in range(len(files_with_class)):
                    for j in range(len(file_has_class)):
                        if i == file_has_class[j]:
                            files_with_class[i] += 1

    def main_code(self):
        for folder in self.folders:
            destination_folders = os.path.join(self.destination_path, folder)
            if not os.path.exists(destination_folders):
                os.mkdir(destination_folders)

        print("Files in directory:")
        # Iterate through the main subdirectories (train, test, valid)
        for folder in self.folders:
            moved_files = 0
            self.not_found_files.clear()
            folder_path = os.path.join(self.source_path, folder)
            if os.path.exists(folder_path):
                # Iterate through the subdirectories within each main folder (images, labels)
                for subfolder in self.subfolders:
                    if subfolder == self.subfolders[1]:
                        subfolder_path = os.path.join(folder_path, subfolder)
                        # List and print the files in the subdirectory
                        if os.path.exists(subfolder_path):
                            for file in os.listdir(subfolder_path):
                                file_path = os.path.join(subfolder_path, file)




                                if os.path.isfile(file_path):
                                    # Iterating through files in 'labels' subfolder
                                    with open(file_path, 'r') as txt_file:
                                        for line in txt_file:
                                            if line[0] == self.class_nr:
                                                image_file_name = file[:-4]
                                                self.txt_files_with_the_class.append(image_file_name)

                                        txt_file.close()
                            destination_images_subfolder = os.path.join(self.destination_path, folder,
                                                                        self.subfolders[0])
                            destination_labels_subfolder = os.path.join(self.destination_path, folder,
                                                                        self.subfolders[1])
                            source_image_folder_path = os.path.join(self.source_path, folder, self.subfolders[0])
                            source_label_folder_path = os.path.join(self.source_path, folder,
                                                                    self.subfolders[1])
                            if not os.path.exists(destination_images_subfolder):
                                os.mkdir(destination_images_subfolder)
                            if not os.path.exists(destination_labels_subfolder):
                                os.mkdir(destination_labels_subfolder)
                            print(f"The file list length -  {len(self.txt_files_with_the_class)}")
                            self.file_data[(len(self.file_data) - none_counter(self.file_data))-1] = len(
                                self.txt_files_with_the_class)
                            for name in self.txt_files_with_the_class:
                                found_file = False
                                for img_file_name, label_file_name in zip(os.listdir(source_image_folder_path),
                                                                          os.listdir(source_label_folder_path)):
                                    if img_file_name.startswith(name):
                                        shutil.copy(os.path.join(subfolder_path, name + ".txt"),
                                                    os.path.join(destination_labels_subfolder, label_file_name))
                                        shutil.copy(os.path.join(source_image_folder_path, img_file_name),
                                                    os.path.join(destination_images_subfolder, img_file_name))
                                        self.txt_files_with_the_class.remove(name)
                                        moved_files += 1
                                        found_file = True
                                        break
                                if not found_file:
                                    self.not_found_files.append(name)
                            print(f"Moved files - {moved_files}")
                            self.file_data[(len(self.file_data) - none_counter(self.file_data))-1] = moved_files
                            self.file_data[(len(self.file_data) - none_counter(self.file_data))-1] = len(
                                self.not_found_files)

            else:
                print(f"Directory {folder_path} does not exist.")

import sys
import random
import string
import uuid
import pydicom
from pydicom.errors import InvalidDicomError
from pydicom.uid import generate_uid
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel,
    QFileDialog, QLineEdit, QHBoxLayout, QWidget, QTextEdit, QMessageBox, QInputDialog
)
import os


class DicomViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.dicom_files = []
        self.dicom_file_paths = []

    def initUI(self):
        self.setWindowTitle("DICOM Viewer")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        # File loader
        self.file_label = QLabel("No file loaded")
        self.load_button = QPushButton("Load DICOM Files or Folder")
        self.load_button.clicked.connect(self.load_files)
        main_layout.addWidget(self.file_label)
        main_layout.addWidget(self.load_button)

        # Display image/video
        self.display_button = QPushButton("Display Image/Video")
        self.display_button.setEnabled(False)
        self.display_button.clicked.connect(self.display_dicom)
        main_layout.addWidget(self.display_button)

        # Display all tags
        self.tags_button = QPushButton("Display All DICOM Tags")
        self.tags_button.setEnabled(False)
        self.tags_button.clicked.connect(self.display_tags)
        main_layout.addWidget(self.tags_button)

        # Display specific groups
        self.specific_button = QPushButton("Display Specific Groups")
        self.specific_button.setEnabled(False)
        self.specific_button.clicked.connect(self.display_specific_groups)
        main_layout.addWidget(self.specific_button)

        # Search tag
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter tag name (e.g., PatientName)")
        self.search_button = QPushButton("Search Tag")
        self.search_button.setEnabled(False)
        self.search_button.clicked.connect(self.search_tag)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        main_layout.addLayout(search_layout)

        # Anonymization
        anonymize_layout = QHBoxLayout()
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("Enter anonymization prefix")
        self.anonymize_button = QPushButton("Anonymize File")
        self.anonymize_button.setEnabled(False)
        self.anonymize_button.clicked.connect(self.anonymize_dicom)
        anonymize_layout.addWidget(self.prefix_input)
        anonymize_layout.addWidget(self.anonymize_button)
        main_layout.addLayout(anonymize_layout)

        # Display 3D as tiles
        self.tile_button = QPushButton("Display 3D as Tiles")
        self.tile_button.setEnabled(False)
        self.tile_button.clicked.connect(self.display_3d_tiles)
        main_layout.addWidget(self.tile_button)

        # Main widget setup
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def load_files(self):
        choice, ok = QInputDialog.getItem(
            self, "Select Load Type", "Choose whether to load a file or folder:",
            ["File", "Folder"], 0, False)

        if ok:
            if choice == "Folder":
                self.load_folder()
            elif choice == "File":
                self.load_file()

    def load_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open DICOM Folder", "", QFileDialog.ShowDirsOnly)
        if folder_path:
            self.load_files_from_folder(folder_path)
        else:
            self.file_label.setText("No folder selected.")

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open DICOM File", "", "DICOM Files (*.dcm *.dicm)")
        if file_path:
            self.load_file_from_path(file_path)
        else:
            self.file_label.setText("No file selected.")

    def load_files_from_folder(self, folder_path):
        try:
            self.dicom_files = []
            self.dicom_file_paths = []
            for file_name in os.listdir(folder_path):
                if file_name.endswith((".dcm", ".dicm")):
                    dicom_path = os.path.join(folder_path, file_name)
                    dicom_file = pydicom.dcmread(dicom_path)
                    self.dicom_files.append(dicom_file)
                    self.dicom_file_paths.append(dicom_path)

            if self.dicom_files:
                self.file_label.setText(f"Loaded {len(self.dicom_files)} DICOM files from folder.")
                self.enable_ui_elements()
            else:
                self.file_label.setText("No DICOM files found in the folder.")
        except Exception as e:
            self.file_label.setText(f"Error loading files: {e}")

    def load_file_from_path(self, file_path):
        try:
            dicom_file = pydicom.dcmread(file_path)
            self.dicom_files = [dicom_file]
            self.dicom_file_paths = [file_path]
            self.file_label.setText(f"Loaded 1 DICOM file: {file_path}")
            self.enable_ui_elements()
        except Exception as e:
            self.file_label.setText(f"Error loading file: {e}")

    def enable_ui_elements(self):
        self.display_button.setEnabled(True)
        self.tags_button.setEnabled(True)
        self.specific_button.setEnabled(True)
        self.search_button.setEnabled(True)
        self.anonymize_button.setEnabled(True)
        self.tile_button.setEnabled(True)

    def display_dicom(self):
        if not self.dicom_files:
            return

        try:
            dicom_file = self.dicom_files[0]
            if getattr(dicom_file, 'NumberOfFrames', 1) > 1:
                play_count = 0  # Counter to track the number of times the video is played
                while play_count < 1:  # Play the video exactly 2 times
                    frames = [dicom_file.pixel_array[i] for i in range(dicom_file.NumberOfFrames)]
                    for frame in frames:
                        frame = np.uint8(frame)
                        cv2.imshow("DICOM Video", frame)
                        if cv2.waitKey(50) & 0xFF == ord('q'):
                            cv2.destroyAllWindows()
                            return  # Exit the function if 'q' is pressed
                    play_count += 1  # Increment the play counter
                cv2.destroyAllWindows()  # Close the window after playing 2 times
            else:
                if len(self.dicom_files) > 1:
                    play_count = 0  # Counter to track the number of times the cine is played
                    while play_count < 1:  # Play the cine exactly 2 times
                        for dicom_file in self.dicom_files:
                            pixel_data = dicom_file.pixel_array
                            if len(pixel_data.shape) == 2:
                                pixel_data = np.uint8(pixel_data)
                                cv2.imshow("DICOM Cine", pixel_data)
                                if cv2.waitKey(50) & 0xFF == ord('q'):
                                    cv2.destroyAllWindows()
                                    return  # Exit the function if 'q' is pressed
                        play_count += 1  # Increment the play counter
                    cv2.destroyAllWindows()  # Close the window after playing 2 times
                else:
                    pixel_data = dicom_file.pixel_array
                    if len(pixel_data.shape) == 2:
                        pixel_data = np.uint8(pixel_data)
                        cv2.imshow("DICOM Image", pixel_data)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
        except Exception as e:
            self.file_label.setText(f"Error displaying image/video: {e}")

    def display_tags(self):
        if not self.dicom_files:
            return

        try:
            tag_info = []
            for dicom_file in self.dicom_files:
                for elem in dicom_file:
                    tag_name = elem.name
                    tag_value = elem.value
                    tag_info.append(f"{tag_name}: {tag_value}")

            self.tag_window = QTextEdit()
            self.tag_window.setWindowTitle("DICOM Tags")
            self.tag_window.setText("\n".join(tag_info))
            self.tag_window.setReadOnly(True)
            self.tag_window.resize(600, 400)
            self.tag_window.show()

        except Exception as e:
            self.file_label.setText(f"Error displaying tags: {e}")

    def display_specific_groups(self):
        if not self.dicom_files:
            return

        try:
            specific_groups = [0x0010, 0x0020, 0x0030]
            group_info = []
            for dicom_file in self.dicom_files:
                for elem in dicom_file:
                    group = elem.tag.group
                    if group in specific_groups:
                        group_info.append(f"{elem.name}: {elem.value}")

            self.group_window = QTextEdit()
            self.group_window.setWindowTitle("Specific Group Tags")
            self.group_window.setText("\n".join(group_info))
            self.group_window.setReadOnly(True)
            self.group_window.resize(600, 400)
            self.group_window.show()
        except Exception as e:
            self.file_label.setText(f"Error displaying specific groups: {e}")

    def search_tag(self):
        if not self.dicom_files:
            return

        try:
            tag_name = self.search_input.text()
            if not tag_name:
                self.file_label.setText("Please enter a tag name.")
                return

            for dicom_file in self.dicom_files:
                for elem in dicom_file:
                    if elem.name == tag_name:
                        self.file_label.setText(f"{tag_name}: {elem.value}")
                        return

            self.file_label.setText(f"Tag '{tag_name}' not found.")
        except Exception as e:
            self.file_label.setText(f"Error searching tag: {e}")

    def anonymize_dicom(self):
        if not self.dicom_files:
            return

        prefix = self.prefix_input.text()
        if not prefix:
            self.file_label.setText("Please enter a prefix for anonymization!")
            return

        critical_fields = ['PatientName', 'PatientID', 'PhysicianName', 'StudyInstanceUID', 'SeriesInstanceUID']
        for dicom_file in self.dicom_files:
            for field in critical_fields:
                if hasattr(dicom_file, field):
                    if field.endswith("UID"):
                        new_uid = generate_uid()
                        setattr(dicom_file, field, new_uid)
                    else:
                        random_value = prefix + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                        setattr(dicom_file, field, random_value)

            save_path, _ = QFileDialog.getSaveFileName(self, "Save Anonymized File", "", "DICOM Files (*.dcm)")
            if save_path:
                dicom_file.save_as(save_path)
                self.file_label.setText(f"Anonymized file saved at: {save_path}")

    def display_3d_tiles(self):
        if not self.dicom_files:
            return

        try:
            # Sort the DICOM files based on file name to display in order (if naming convention is sequential)
            self.dicom_files.sort(key=lambda x: x.filename)

            num_slices = 11
            cols = 5  # Calculate number of columns for display
            rows = 3  # Calculate number of rows for display

            fig, axes = plt.subplots(rows, cols, figsize=(15, 15))
            axes = axes.flatten()

            for i, ax in enumerate(axes):
                if i < num_slices:
                    dicom_file = self.dicom_files[i]
                    pixel_data = dicom_file.pixel_array
                    ax.imshow(pixel_data, cmap="gray")
                    ax.axis("off")
                    ax.set_title(f"Slice {i + 1}")
                else:
                    ax.axis("off")  # Hide unused axes

            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.file_label.setText(f"Error displaying 3D tiles: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = DicomViewer()
    viewer.show()
    sys.exit(app.exec_())

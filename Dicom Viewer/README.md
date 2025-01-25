# DICOM Viewer

A Python-based DICOM viewer application built using PyQt5 and pydicom. This application allows you to load, view, and manipulate DICOM files, including displaying images, videos, and 3D slices. It also supports anonymization of DICOM files and searching for specific DICOM tags.

---

## Features

- **Load DICOM Files or Folders**: Load individual DICOM files or entire folders containing DICOM files.
- **Display Images and Videos**: View DICOM images and videos directly within the application.
- **Display DICOM Tags**: View all DICOM tags or specific groups of tags.
- **Search for Tags**: Search for specific DICOM tags by name.
- **Anonymize DICOM Files**: Anonymize DICOM files by replacing sensitive information with random values.
- **Display 3D Slices as Tiles**: Display 3D DICOM data as a grid of 2D slices.

---

## Requirements

- Python 3.7 or higher
- PyQt5
- pydicom
- numpy
- opencv-python
- matplotlib

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dicom-viewer.git
   cd dicom-viewer
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python dicom_viewer.py
   ```

---

## Usage

- **Load DICOM Files or Folders**:
  - Click on "Load DICOM Files or Folder" to load individual DICOM files or an entire folder containing DICOM files.

- **Display Images/Videos**:
  - After loading the DICOM files, click on "Display Image/Video" to view the DICOM image or video.
   ![image](https://github.com/user-attachments/assets/86211910-43de-481c-afcd-3bc14396ec88)

- **Display DICOM Tags**:
  - Click on "Display All DICOM Tags" to view all the tags in the loaded DICOM files.
  - Click on "Display Specific Groups" to view tags from specific groups (e.g., Patient, Study, Series).
    ![image](https://github.com/user-attachments/assets/b752f184-5074-4aa6-8c5c-859ffb5567c7)

- **Search for Tags**:
  - Enter the tag name (e.g., `PatientName`) in the search box and click "Search Tag" to find and display the value of the specified tag.
    ![image](https://github.com/user-attachments/assets/1b1c90ba-f09e-4e3b-a91f-90a88d9e2cd7)


- **Anonymize DICOM Files**:
  - Enter a prefix in the anonymization input box and click "Anonymize File" to anonymize the loaded DICOM files. The anonymized files will be saved to a location of your choice.
    ![image](https://github.com/user-attachments/assets/70f3a5a7-a0b1-4591-88c5-cff830158f30)

- **Display 3D Slices as Tiles**:
  - Click on "Display 3D as Tiles" to view 3D DICOM data as a grid of 2D slices.
    ![image](https://github.com/user-attachments/assets/731c9755-d987-4a26-ad58-ece6a4651886)

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue if you find any bugs or have suggestions for improvements.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgments

- **PyQt5** for the GUI framework.
- **pydicom** for DICOM file handling.
- **OpenCV** for image and video display.
- **Matplotlib** for displaying 3D slices.

---


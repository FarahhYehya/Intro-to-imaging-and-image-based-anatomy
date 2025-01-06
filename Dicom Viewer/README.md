# DICOM Viewer

A Python-based DICOM viewer application built using PyQt5 and pydicom. This application allows you to load, view, and manipulate DICOM files, including displaying images, videos, and 3D slices. It also supports anonymization of DICOM files and searching for specific DICOM tags.

## Features

- **Load DICOM Files or Folders**: Load individual DICOM files or entire folders containing DICOM files.
- **Display Images and Videos**: View DICOM images and videos directly within the application.
- **Display DICOM Tags**: View all DICOM tags or specific groups of tags.
- **Search for Tags**: Search for specific DICOM tags by name.
- **Anonymize DICOM Files**: Anonymize DICOM files by replacing sensitive information with random values.
- **Display 3D Slices as Tiles**: Display 3D DICOM data as a grid of 2D slices.

## Requirements

- Python 3.7 or higher
- PyQt5
- pydicom
- numpy
- opencv-python
- matplotlib

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/dicom-viewer.git
   cd dicom-viewer
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python dicom_viewer.py
   ```

## Usage

1. **Load DICOM Files or Folders**:
   - Click on "Load DICOM Files or Folder" to load individual DICOM files or an entire folder containing DICOM files.

2. **Display Images/Videos**:
   - After loading the DICOM files, click on "Display Image/Video" to view the DICOM image or video.

3. **Display DICOM Tags**:
   - Click on "Display All DICOM Tags" to view all the tags in the loaded DICOM files.
   - Click on "Display Specific Groups" to view tags from specific groups (e.g., Patient, Study, Series).

4. **Search for Tags**:
   - Enter the tag name (e.g., `PatientName`) in the search box and click "Search Tag" to find and display the value of the specified tag.

5. **Anonymize DICOM Files**:
   - Enter a prefix in the anonymization input box and click "Anonymize File" to anonymize the loaded DICOM files. The anonymized files will be saved to a location of your choice.

6. **Display 3D Slices as Tiles**:
   - Click on "Display 3D as Tiles" to view 3D DICOM data as a grid of 2D slices.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- [PyQt5](https://pypi.org/project/PyQt5/) for the GUI framework.
- [pydicom](https://pypi.org/project/pydicom/) for DICOM file handling.
- [OpenCV](https://opencv.org/) for image and video display.
- [Matplotlib](https://matplotlib.org/) for displaying 3D slices.

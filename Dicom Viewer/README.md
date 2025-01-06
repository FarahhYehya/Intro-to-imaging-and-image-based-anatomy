# DICOM Viewer

A Python-based DICOM viewer application built using PyQt5 and pydicom. This application allows users to load, view, and manipulate DICOM files, including displaying images, videos, and 3D slices. It also supports anonymization of DICOM files and searching for specific DICOM tags.

## Features

- **Load DICOM Files or Folders**: Load individual DICOM files or entire folders containing DICOM files.
- **Display Images/Video**: View DICOM images or videos directly within the application.
- **Display All DICOM Tags**: View all metadata tags associated with the loaded DICOM files.
- **Display Specific Groups**: Display tags from specific DICOM groups (e.g., Patient, Study, Series).
- **Search Tags**: Search for specific DICOM tags by name.
- **Anonymize DICOM Files**: Anonymize critical patient information in DICOM files.
- **Display 3D as Tiles**: Display 3D DICOM data as a grid of 2D slices.

## Requirements

- Python 3.7+
- PyQt5
- pydicom
- numpy
- opencv-python
- matplotlib

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/dicom-viewer.git
   cd dicom-viewer

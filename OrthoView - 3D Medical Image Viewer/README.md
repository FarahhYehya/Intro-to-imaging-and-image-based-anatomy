# OrthoView - 3D Medical Image Viewer

## Overview
OrthoView is a Python-based 3D medical image viewer designed for visualizing DICOM files in three orthogonal planes: sagittal, coronal, and transverse. Built with PyQt5, this application provides an intuitive interface for navigating through medical imaging data, adjusting image properties, and exploring cross-sectional views. It is ideal for medical professionals, researchers, and students working with DICOM datasets.

## Features
- **Three Orthogonal Views**: Visualize DICOM data in sagittal, coronal, and transverse planes simultaneously.
- **Brightness and Contrast Adjustment**: Fine-tune image appearance using dedicated sliders.
- **Slice Navigation**: Easily navigate through slices in each plane using interactive sliders.
- **Crosshair Visualization**: Crosshairs in each view indicate the corresponding slice positions in the other two views.
- **Zoom and Pan**: Use the built-in navigation toolbar to zoom in/out and pan across images.
- **DICOM File Loading**: Load and display DICOM files from a selected directory.
- **Interactive Slice Selection**: Click on any point in one view to update the slice positions in the other views.

## Video Demonstration
Below is a screen recording of OrthoView in action:

![OrthoView Demo(https://github.com/user-attachments/assets/0770c280-f844-4ddc-bc47-fff16e7ec9e5).

This video demonstrates:
1. Loading DICOM files.
2. Navigating through slices in sagittal, coronal, and transverse planes.
3. Adjusting brightness and contrast.
4. Using crosshairs to synchronize views.
5. Zooming and panning across images.

## Requirements
To run OrthoView, ensure the following Python packages are installed:

- PyQt5
- pydicom
- numpy
- matplotlib

You can install these packages using pip:

```bash
pip install PyQt5 pydicom numpy matplotlib
```

## Usage
1. **Launch the Application**:
   - Run the script by executing:
     ```bash
     python main.py
     ```
   - The OrthoView application window will open.

2. **Load DICOM Files**:
   - Click the "Upload DICOM Files" button or use the "Open" option in the "File" menu.
   - Select a directory containing DICOM files. The application will load and display the DICOM series.

3. **Navigate Through Slices**:
   - Use the sliders below each view to navigate through the slices in the sagittal, coronal, and transverse planes.

   - ![WhatsApp Image 2025-01-25 at 17 22 00_3bec0cb4](https://github.com/user-attachments/assets/4fef2714-1ba0-478a-9ddd-903dc22444ed)

4. **Adjust Brightness and Contrast**:
   - Use the brightness and contrast sliders at the bottom of the window to adjust the image appearance for better visualization.

   - ![WhatsApp Image 2025-01-25 at 17 22 01_bb424331](https://github.com/user-attachments/assets/5c859213-5929-4c49-97a2-74dbc5f1091a)


5. **Zoom and Pan**:
   - Use the navigation toolbar above each view to zoom in/out and pan across the image.

6. **Crosshair Navigation**:
   - Click on any point in one view to update the slice positions in the other two views. Crosshairs will indicate the corresponding positions.

     ![WhatsApp Image 2025-01-25 at 17 22 01_bf280740](https://github.com/user-attachments/assets/2007e5ac-bbd8-460a-81f3-e3f93742bf6e)


## Code Structure
- **OrthoView Class**:
  - The main class that sets up the GUI and handles DICOM file loading, slice navigation, and image display.
  - Contains methods for updating views, handling mouse clicks, and adjusting brightness and contrast.

- **Main Function**:
  - Initializes the PyQt application and starts the OrthoView application.

## Key Methods
- `load_dicom()`: Loads DICOM files from a selected directory and initializes the 3D volume.
- `update_all_views()`: Updates all three views (sagittal, coronal, transverse) based on the current slice positions.
- `update_view(view_type)`: Updates a specific view with the current slice data, applying brightness and contrast adjustments.
- `on_click(event, view_type)`: Handles mouse clicks to update slice positions in the other views.
- `update_brightness()` and `update_contrast()`: Adjust the brightness and contrast of the displayed images.

## Example Workflow
1. Load a DICOM series by selecting a directory containing the files.
2. Scroll through the slices using the sliders in each view.
3. Click on a point in the sagittal view to see the corresponding slices in the coronal and transverse views.
4. Adjust the brightness and contrast to enhance the visibility of anatomical structures.
5. Use the zoom and pan tools to explore specific regions of interest.

## Notes
- Ensure that the selected directory contains valid DICOM files. The application will display an error message if no DICOM files are found.
- The application assumes that the DICOM files are sorted by slice location. If the files do not have a `SliceLocation` attribute, they are sorted by their order in the directory.

## License
This code is provided under the MIT License.

OrthoView is a powerful tool for exploring and analyzing 3D medical imaging data. Whether you're a medical professional, researcher, or student, this application provides an easy-to-use interface for visualizing DICOM datasets in multiple planes. Enjoy exploring your medical images with OrthoView!

---

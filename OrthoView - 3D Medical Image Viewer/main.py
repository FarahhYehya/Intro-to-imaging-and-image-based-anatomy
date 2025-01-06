import sys
import os
import numpy as np
import pydicom
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QSlider, QLabel, QFileDialog, QPushButton,
                             QProgressDialog, QMessageBox, QGridLayout)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class DicomViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('3D DICOM Viewer')
        self.setGeometry(100, 100, 1400, 900)

        # Initialize variables
        self.volume = None
        self.current_slice = {"sagittal": 0, "coronal": 0, "transverse": 0}
        self.brightness = 0.0  # Changed initial value to 0
        self.contrast = 1.0  # Keep initial contrast at 1

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Add upload button at the top
        upload_layout = QHBoxLayout()
        upload_button = QPushButton("Upload DICOM Files")
        upload_button.clicked.connect(self.load_dicom)
        upload_layout.addWidget(upload_button)
        layout.addLayout(upload_layout)

        # Create display area with navigation sliders
        display_layout = QGridLayout()

        # Create the three view panels with navigation sliders
        self.views = {}
        self.nav_sliders = {}
        self.toolbars = {}  # Add storage for toolbars

        for i, view_type in enumerate(["sagittal", "coronal", "transverse"]):
            # Create view container
            view_container = QVBoxLayout()

            # Add view label
            view_label = QLabel(f"{view_type.capitalize()} View")
            view_label.setAlignment(Qt.AlignCenter)
            view_container.addWidget(view_label)

            # Create figure and canvas
            fig = Figure(figsize=(4, 4))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            self.views[view_type] = {"figure": fig, "canvas": canvas, "ax": ax}

            # Add toolbar for zoom functionality
            toolbar = NavigationToolbar(canvas, self)
            self.toolbars[view_type] = toolbar
            view_container.addWidget(toolbar)
            view_container.addWidget(canvas)

            # Add navigation slider
            slider_layout = QHBoxLayout()
            slider_label = QLabel("Slice:")
            self.nav_sliders[view_type] = QSlider(Qt.Horizontal)
            self.nav_sliders[view_type].setEnabled(False)
            self.nav_sliders[view_type].valueChanged.connect(
                lambda value, vt=view_type: self.update_slice_position(value, vt))

            slider_layout.addWidget(slider_label)
            slider_layout.addWidget(self.nav_sliders[view_type])
            view_container.addLayout(slider_layout)

            # Add to grid layout
            display_layout.addLayout(view_container, 0, i)

            # Connect mouse events
            canvas.mpl_connect('button_press_event',
                               lambda event, vt=view_type: self.on_click(event, vt))

        layout.addLayout(display_layout)

        # Create controls
        controls_layout = QHBoxLayout()

        # Brightness slider
        brightness_layout = QVBoxLayout()
        brightness_label = QLabel("Brightness:")
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(-100)  # Changed range to be centered at 0
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(0)  # Start at middle (no brightness adjustment)
        self.brightness_slider.valueChanged.connect(self.update_brightness)
        brightness_layout.addWidget(brightness_label)
        brightness_layout.addWidget(self.brightness_slider)
        controls_layout.addLayout(brightness_layout)

        # Contrast slider
        contrast_layout = QVBoxLayout()
        contrast_label = QLabel("Contrast:")
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(1)  # Changed minimum to 1 to avoid division by zero
        self.contrast_slider.setMaximum(200)
        self.contrast_slider.setValue(100)  # Start at middle (normal contrast)
        self.contrast_slider.valueChanged.connect(self.update_contrast)
        contrast_layout.addWidget(contrast_label)
        contrast_layout.addWidget(self.contrast_slider)
        controls_layout.addLayout(contrast_layout)

        layout.addLayout(controls_layout)

        # Add menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        open_action = file_menu.addAction('Open')
        open_action.triggered.connect(self.load_dicom)

    def update_slice_position(self, value, view_type):
        """Update the current slice position for the given view"""
        self.current_slice[view_type] = value
        self.update_all_views()

    def load_dicom(self):
        """Load DICOM series from a directory"""
        try:
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.DontUseNativeDialog, True)
            dialog.setOption(QFileDialog.ShowDirsOnly, False)

            if dialog.exec_():
                directory = dialog.selectedFiles()[0]

                if not os.path.isdir(directory):
                    QMessageBox.warning(self, "Error", "Please select a valid directory")
                    return

                # Get all DICOM files in the directory
                dicom_files = []
                for root, _, files in os.walk(directory):
                    for file in files:
                        try:
                            if pydicom.misc.is_dicom(os.path.join(root, file)):
                                dicom_files.append(os.path.join(root, file))
                        except:
                            continue

                if not dicom_files:
                    QMessageBox.warning(self, "Error", "No DICOM files found in the selected directory")
                    return

                # Create progress dialog
                progress = QProgressDialog("Loading DICOM files...", "Cancel", 0, len(dicom_files), self)
                progress.setWindowModality(Qt.WindowModal)

                # Load all DICOM files
                slices = []
                for i, file in enumerate(dicom_files):
                    if progress.wasCanceled():
                        return

                    dcm = pydicom.dcmread(file)
                    slices.append((dcm.SliceLocation if hasattr(dcm, 'SliceLocation') else i,
                                   dcm.pixel_array))
                    progress.setValue(i)

                # Sort slices by location
                slices.sort(key=lambda x: x[0])

                # Stack slices into 3D volume
                self.volume = np.stack([slice[1] for slice in slices])

                # Update slider ranges based on volume dimensions
                self.nav_sliders["sagittal"].setRange(0, self.volume.shape[0] - 1)
                self.nav_sliders["coronal"].setRange(0, self.volume.shape[1] - 1)
                self.nav_sliders["transverse"].setRange(0, self.volume.shape[2] - 1)

                # Enable sliders
                for slider in self.nav_sliders.values():
                    slider.setEnabled(True)

                # Set initial slice positions to middle of each dimension
                for view_type in self.current_slice:
                    if view_type == "sagittal":
                        mid = self.volume.shape[0] // 2
                    elif view_type == "coronal":
                        mid = self.volume.shape[1] // 2
                    else:  # transverse
                        mid = self.volume.shape[2] // 2
                    self.current_slice[view_type] = mid
                    self.nav_sliders[view_type].setValue(mid)

                self.update_all_views()

                # Show success message
                QMessageBox.information(self, "Success",
                                        f"Successfully loaded {len(dicom_files)} DICOM files")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading DICOM files: {str(e)}")

    def update_all_views(self):
        """Update all three views"""
        if self.volume is None:
            return

        for view_type in ["sagittal", "coronal", "transverse"]:
            self.update_view(view_type)

    def update_view(self, view_type):
        """Update a specific view"""
        if self.volume is None:
            return

        ax = self.views[view_type]["ax"]
        ax.clear()

        # Get the appropriate slice based on view type
        if view_type == "sagittal":
            slice_data = self.volume[self.current_slice["sagittal"], :, :].copy()  # Make a copy
        elif view_type == "coronal":
            slice_data = self.volume[:, self.current_slice["coronal"], :].copy()
        else:  # transverse
            slice_data = self.volume[:, :, self.current_slice["transverse"]].copy()

        # Normalize the data to 0-1 range for better brightness/contrast control
        if slice_data.max() != slice_data.min():
            slice_data = (slice_data - slice_data.min()) / (slice_data.max() - slice_data.min())

        # Apply contrast first, then brightness
        slice_data = np.clip(slice_data * self.contrast + self.brightness, 0, 1)

        # Display the slice
        ax.imshow(slice_data, cmap='gray', vmin=0, vmax=1)

        # Draw crosshair at current position
        if view_type == "sagittal":
            ax.axhline(y=self.current_slice["coronal"], color='r', alpha=0.5)
            ax.axvline(x=self.current_slice["transverse"], color='r', alpha=0.5)
        elif view_type == "coronal":
            ax.axhline(y=self.current_slice["sagittal"], color='r', alpha=0.5)
            ax.axvline(x=self.current_slice["transverse"], color='r', alpha=0.5)
        else:  # transverse
            ax.axhline(y=self.current_slice["sagittal"], color='r', alpha=0.5)
            ax.axvline(x=self.current_slice["coronal"], color='r', alpha=0.5)

        self.views[view_type]["canvas"].draw()

    def on_click(self, event, view_type):
        """Handle mouse clicks on the views"""
        if event.inaxes is None:
            return

        x, y = int(event.xdata), int(event.ydata)

        # Update current slices based on which view was clicked
        if view_type == "sagittal":
            self.current_slice["coronal"] = y
            self.current_slice["transverse"] = x
        elif view_type == "coronal":
            self.current_slice["sagittal"] = y
            self.current_slice["transverse"] = x
        else:  # transverse
            self.current_slice["sagittal"] = y
            self.current_slice["coronal"] = x

        self.update_all_views()

    def update_brightness(self):
        """Update brightness based on slider value"""
        self.brightness = self.brightness_slider.value() / 100.0  # Convert to -1.0 to 1.0 range
        self.update_all_views()

    def update_contrast(self):
        """Update contrast based on slider value"""
        self.contrast = self.contrast_slider.value() / 50.0  # Convert to 0.02 to 4.0 range
        self.update_all_views()


def main():
    app = QApplication(sys.argv)
    viewer = DicomViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
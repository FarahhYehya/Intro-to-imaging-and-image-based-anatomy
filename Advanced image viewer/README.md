# Advanced Image Viewer

A Python-based GUI application for image processing and analysis. Built with `Tkinter`, `OpenCV`, and `Matplotlib`, this tool allows you to load, process, and analyze images with ease.

---

## Features

- **Load and Save Images**: Supports JPG, JPEG, PNG, and BMP formats.
- **Image Processing**:
  - Add noise: Gaussian, Salt-and-Pepper, Speckle.
  - Denoise: Gaussian, Median, Bilateral.
  - Apply filters: Lowpass, Highpass, Sharpen, Edge Detection.
  - Enhance contrast: Histogram Equalization, CLAHE, Gamma Correction.
- **ROI Selection**: Draw regions of interest (ROIs) for signal and noise analysis.
- **SNR/CNR Calculation**: Compute Signal-to-Noise Ratio (SNR) and Contrast-to-Noise Ratio (CNR).
- **Zoom and Resolution Control**: Adjust zoom level, interpolation, and pixel density.
- **Brightness/Contrast Adjustment**: Fine-tune using sliders.
- **Field of View (FOV)**: Set a custom FOV center and size.
- **Histogram Visualization**: Double-click any image to view its histogram.
- **Undo/Reset**: Revert changes or reset the application.

---

## Video Demonstration

Here’s a quick demo of the Advanced Image Viewer in action:


### Video Example
[![Advanced Image Viewer Demo](https://github.com/user-attachments/assets/5ea78773-0308-4f11-a601-2d9a0fb08883)

---

## Requirements

Install the required libraries:

```bash
pip install opencv-python numpy matplotlib Pillow
```

---

## How to Use

1. **Run the Application**:
   ```bash
   python image_viewer.py
   ```

2. **Load an Image**:
   - Click **Open Image** to load an image.

3. **Process the Image**:
   - Use the **Controls** panel to add noise, apply filters, or enhance contrast.
   - Adjust brightness and contrast with sliders.

4. **Select ROIs**:
   - Click **Select ROI 1**, **Select ROI 2**, or **Select Noise ROI** to draw rectangles on the image.
   - Click **Calculate SNR** or **Calculate CNR** to compute ratios.

5. **Adjust Zoom and FOV**:
   - Use the **Zoom Type** dropdown and **Zoom Scale** slider.
   - Set a custom FOV center and size.

6. **View Histogram**:
   - Double-click any image to view its histogram.

7. **Save the Image**:
   - Click **Save Output** to save the processed image.

8. **Undo/Reset**:
   - Use **Undo** to revert the last operation.
   - Use **Reset** to clear all images and settings.

---

## Code Overview

- **`ImageViewer` Class**: Handles the GUI and image processing logic.
- **GUI Components**:
  - **Viewports**: Display input and output images.
  - **Control Panel**: Buttons, sliders, and dropdowns for processing.
- **Image Processing**: Implemented using OpenCV.
- **ROI and SNR/CNR**: Selected by drawing rectangles; calculations use mean and standard deviation.

---

## Example Workflow

1. Load an image.
2. Add Gaussian noise and apply Median denoising.
3. Select ROIs for signal and noise.
4. Calculate SNR and CNR.
5. Adjust brightness/contrast.
6. Set and apply FOV.
7. Save the processed image.

---

## License

MIT License.

---


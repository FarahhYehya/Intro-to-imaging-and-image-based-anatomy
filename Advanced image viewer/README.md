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
https://github.com/user-attachments/assets/5ea78773-0308-4f11-a601-2d9a0fb08883

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

![WhatsApp Image 2025-01-25 at 17 25 55_26587b79](https://github.com/user-attachments/assets/6c124a45-75b1-45e2-9402-0f0e1998b550)

![WhatsApp Image 2025-01-25 at 17 25 56_2d2e1cf2](https://github.com/user-attachments/assets/a269a860-e41d-48ce-a010-3e2f1a06cd9d)


4. **Select ROIs**:
   - Click **Select ROI 1**, **Select ROI 2**, or **Select Noise ROI** to draw rectangles on the image.
   - Click **Calculate SNR** or **Calculate CNR** to compute ratios.

     ![WhatsApp Image 2025-01-25 at 17 25 56_6082b4c1](https://github.com/user-attachments/assets/37753b5e-d2e9-4eca-b844-a3a7326949fd)

5. **Adjust Zoom and FOV**:
   - Use the **Zoom Type** dropdown and **Zoom Scale** slider.
   - Set a custom FOV center and size.

   ![WhatsApp Image 2025-01-25 at 17 25 56_0937c398](https://github.com/user-attachments/assets/ae7c3310-1a2a-42d9-8d1c-36ef5e4dc956)

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


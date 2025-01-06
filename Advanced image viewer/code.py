import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


class ImageViewer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Image Viewer")
        self.root.geometry("1400x900")

        self.input_image = None
        self.output1_image = None
        self.output2_image = None
        self.current_image = None
        self.roi1 = None
        self.roi2 = None
        self.noise_roi = None
        self.drawing = False
        self.start_point = None
        self.current_rectangle = None
        self.current_roi_type = None
        self.fov_center = None
        self.rectangle_ids = {"input": None, "output1": None, "output2": None}  # Store rectangle IDs
        self.setup_gui()

    def setup_gui(self):
        # Viewports
        self.input_canvas = self.create_viewport("Input", row=0, column=0)
        self.output1_canvas = self.create_viewport("Output 1", row=0, column=1)
        self.output2_canvas = self.create_viewport("Output 2", row=0, column=2)

        # Control Panel
        control_frame = ttk.LabelFrame(self.root, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # File Operations
        ttk.Button(control_frame, text="Open Image", command=self.open_image).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(control_frame, text="Save Output", command=self.save_image).grid(row=0, column=1, padx=5, pady=5)

        # Source Selection Box
        ttk.Label(control_frame, text="Source:").grid(row=0, column=2, padx=5, pady=5)
        self.source_var = tk.StringVar(value="Input")
        ttk.Combobox(control_frame, textvariable=self.source_var,
                     values=["Input", "Output 1", "Output 2"]).grid(row=0, column=3, padx=5, pady=5)

        # Zoom and Interpolation
        ttk.Label(control_frame, text="Zoom Type:").grid(row=1, column=0, padx=5, pady=5)
        self.zoom_type_var = tk.StringVar(value="Linear")
        ttk.Combobox(control_frame, textvariable=self.zoom_type_var,
                     values=["Nearest", "Linear", "Bilinear", "Bicubic", "Area"]).grid(row=1, column=1, padx=5, pady=5)

        # Output Resolution Slider
        ttk.Label(control_frame, text="Zoom scale: ").grid(row=1, column=2, padx=5, pady=5)
        self.resolution_slider = ttk.Scale(control_frame, from_=100, to=1000, orient="horizontal", length=150,
                                           command=lambda _: self.apply_resolution())
        self.resolution_slider.set(400)  # Default resolution (400x400)
        self.resolution_slider.grid(row=1, column=3, padx=5, pady=5)

        # No of Pixels Slider
        ttk.Label(control_frame, text="No of Pixels:").grid(row=1, column=4, padx=5, pady=5)
        self.pixels_slider = ttk.Scale(control_frame, from_=1, to=100, orient="horizontal", length=150,
                                       command=lambda _: self.apply_pixels())
        self.pixels_slider.set(50)  # Default value
        self.pixels_slider.grid(row=1, column=5, padx=5, pady=5)

        # Noise and Denoising
        ttk.Label(control_frame, text="Noise:").grid(row=2, column=0, padx=5, pady=5)
        self.noise_var = tk.StringVar(value="None")
        ttk.Combobox(control_frame, textvariable=self.noise_var,
                     values=["None", "Gaussian", "Salt-and-Pepper", "Speckle"]).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(control_frame, text="Denoise:").grid(row=2, column=2, padx=5, pady=5)
        self.denoise_var = tk.StringVar(value="None")
        ttk.Combobox(control_frame, textvariable=self.denoise_var,
                     values=["None", "Gaussian", "Median", "Bilateral"]).grid(row=2, column=3, padx=5, pady=5)
        ttk.Button(control_frame, text="Apply Noise/Denoise", command=self.apply_noise_denoise).grid(row=2, column=4,
                                                                                                     padx=5, pady=5)

        # Filters
        ttk.Label(control_frame, text="Filter:").grid(row=3, column=0, padx=5, pady=5)
        self.filter_var = tk.StringVar(value="None")
        ttk.Combobox(control_frame, textvariable=self.filter_var,
                     values=["None", "Lowpass", "Highpass", "Sharpen", "Edge Detection"]).grid(row=3, column=1, padx=5,
                                                                                               pady=5)
        ttk.Button(control_frame, text="Apply Filter", command=self.apply_filter).grid(row=3, column=2, padx=5, pady=5)

        # Contrast Enhancement
        ttk.Label(control_frame, text="Contrast:").grid(row=4, column=0, padx=5, pady=5)
        self.contrast_var = tk.StringVar(value="None")
        ttk.Combobox(control_frame, textvariable=self.contrast_var,
                     values=["None", "Histogram Equalization", "CLAHE", "Gamma Correction"]).grid(row=4, column=1,
                                                                                                  padx=5, pady=5)
        ttk.Button(control_frame, text="Apply Contrast", command=self.apply_contrast).grid(row=4, column=2, padx=5,
                                                                                           pady=5)

        # ROI and SNR
        ttk.Button(control_frame, text="Select ROI 1 (Signal 1)", command=lambda: self.select_roi("roi1")).grid(row=5,
                                                                                                                column=0,
                                                                                                                padx=5,
                                                                                                                pady=5)
        ttk.Button(control_frame, text="Select ROI 2 (Signal 2)", command=lambda: self.select_roi("roi2")).grid(row=5,
                                                                                                                column=1,
                                                                                                                padx=5,
                                                                                                                pady=5)
        ttk.Button(control_frame, text="Select Noise ROI", command=lambda: self.select_roi("noise_roi")).grid(row=5,
                                                                                                              column=2,
                                                                                                              padx=5,
                                                                                                              pady=5)
        ttk.Button(control_frame, text="Calculate SNR", command=self.calculate_snr).grid(row=5, column=3, padx=5,
                                                                                         pady=5)
        ttk.Button(control_frame, text="Calculate CNR", command=self.calculate_cnr).grid(row=5, column=4, padx=5,
                                                                                         pady=5)
        self.snr_label = ttk.Label(control_frame, text="SNR: N/A")
        self.snr_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.cnr_label = ttk.Label(control_frame, text="CNR: N/A")
        self.cnr_label.grid(row=6, column=2, columnspan=2, padx=5, pady=5)

        # Brightness and Contrast Adjustment
        ttk.Label(control_frame, text="Brightness:").grid(row=7, column=0, padx=5, pady=5)
        self.brightness_slider = ttk.Scale(control_frame, from_=-100, to=100, orient="horizontal", length=150)
        self.brightness_slider.set(0)
        self.brightness_slider.grid(row=7, column=1, padx=5, pady=5)
        ttk.Label(control_frame, text="Contrast:").grid(row=7, column=2, padx=5, pady=5)
        self.contrast_slider = ttk.Scale(control_frame, from_=-100, to=100, orient="horizontal", length=150)
        self.contrast_slider.set(0)
        self.contrast_slider.grid(row=7, column=3, padx=5, pady=5)
        ttk.Button(control_frame, text="Apply Brightness/Contrast", command=self.apply_brightness_contrast).grid(row=7,
                                                                                                                 column=4,
                                                                                                                 padx=5,
                                                                                                                 pady=5)

        # FOV
        ttk.Button(control_frame, text="Set FOV Center", command=self.set_fov_center).grid(row=8, column=0, padx=5,
                                                                                           pady=5)
        ttk.Label(control_frame, text="FOV Size:").grid(row=8, column=1, padx=5, pady=5)
        self.fov_slider = ttk.Scale(control_frame, from_=10, to=100, orient="horizontal", length=150)
        self.fov_slider.set(100)
        self.fov_slider.grid(row=8, column=2, padx=5, pady=5)
        ttk.Button(control_frame, text="Apply FOV", command=self.apply_fov).grid(row=8, column=3, padx=5, pady=5)

        # Apply to Output
        ttk.Label(control_frame, text="Apply to:").grid(row=9, column=0, padx=5, pady=5)
        self.apply_to_var = tk.StringVar(value="Output 1")
        ttk.Combobox(control_frame, textvariable=self.apply_to_var, values=["Output 1", "Output 2"]).grid(row=9,
                                                                                                          column=1,
                                                                                                          padx=5,
                                                                                                          pady=5)

        # Undo and Reset
        ttk.Button(control_frame, text="Undo", command=self.undo).grid(row=10, column=0, padx=5, pady=5)
        ttk.Button(control_frame, text="Reset", command=self.reset).grid(row=10, column=1, padx=5, pady=5)

        # Bind mouse events for ROI selection
        self.input_canvas.bind("<ButtonPress-1>", self.start_draw_roi)
        self.input_canvas.bind("<B1-Motion>", self.draw_roi)
        self.input_canvas.bind("<ButtonRelease-1>", self.end_draw_roi)

        self.output1_canvas.bind("<ButtonPress-1>", self.start_draw_roi)
        self.output1_canvas.bind("<B1-Motion>", self.draw_roi)
        self.output1_canvas.bind("<ButtonRelease-1>", self.end_draw_roi)

        self.output2_canvas.bind("<ButtonPress-1>", self.start_draw_roi)
        self.output2_canvas.bind("<B1-Motion>", self.draw_roi)
        self.output2_canvas.bind("<ButtonRelease-1>", self.end_draw_roi)

    def create_viewport(self, title, row, column):
        frame = ttk.LabelFrame(self.root, text=title, padding="10")
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        canvas = tk.Canvas(frame, width=400, height=400, bg="white")
        canvas.pack()
        canvas.bind("<Double-Button-1>", self.show_histogram)
        return canvas

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.input_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if self.input_image is None:
                messagebox.showerror("Error", "Failed to load image.")
                return
            self.display_image(self.input_image, self.input_canvas)

    def save_image(self):
        if self.output2_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                cv2.imwrite(file_path, self.output2_image)

    def display_image(self, image, canvas):
        if image is None:
            return

        # Get canvas dimensions
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Resize the image to fit within the canvas while maintaining aspect ratio
        height, width = image.shape
        aspect_ratio = width / height

        if aspect_ratio > 1:  # Width > Height
            new_width = min(canvas_width, width)
            new_height = int(new_width / aspect_ratio)
        else:  # Height >= Width
            new_height = min(canvas_height, height)
            new_width = int(new_height * aspect_ratio)

        # Resize the image
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

        # Convert to PIL format and display
        image_pil = Image.fromarray(resized_image)
        image_tk = ImageTk.PhotoImage(image_pil)
        canvas.image = image_tk
        canvas.create_image(0, 0, anchor="nw", image=image_tk)

    def show_histogram(self, event):
        if event.widget == self.input_canvas:
            image = self.input_image
        elif event.widget == self.output1_canvas:
            image = self.output1_image
        elif event.widget == self.output2_canvas:
            image = self.output2_image
        else:
            return

        if image is not None:
            plt.hist(image.ravel(), bins=256, range=(0, 256), color="black")
            plt.title("Histogram")
            plt.xlabel("Pixel Intensity")
            plt.ylabel("Frequency")
            plt.show()

    def apply_zoom(self):
        if self.input_image is None:
            return

        # Get zoom level and type
        zoom_level = self.zoom_slider.get() / 100
        zoom_type = self.zoom_type_var.get()

        # Map zoom types to cv2 constants
        interpolation_methods = {
            "Nearest": cv2.INTER_NEAREST,
            "Linear": cv2.INTER_LINEAR,
            "Bilinear": cv2.INTER_CUBIC,  # Note: Bilinear is typically INTER_LINEAR
            "Bicubic": cv2.INTER_CUBIC,
            "Area": cv2.INTER_AREA
        }

        # Get selected interpolation method
        interpolation = interpolation_methods.get(zoom_type, cv2.INTER_LINEAR)

        # Resize the image based on zoom level
        height, width = self.input_image.shape
        new_width = int(width * zoom_level)
        new_height = int(height * zoom_level)

        # If FOV is set, crop and resize the FOV
        if self.fov_center is not None:
            fov_size = self.fov_slider.get() / 100
            fov_width = int(width * fov_size)
            fov_height = int(height * fov_size)

            # Scale FOV center to image coordinates
            canvas_width = self.input_canvas.winfo_width()
            canvas_height = self.input_canvas.winfo_height()
            x = int(self.fov_center[0] * width / canvas_width)
            y = int(self.fov_center[1] * height / canvas_height)

            # Calculate crop boundaries
            start_x = max(0, x - fov_width // 2)
            start_y = max(0, y - fov_height // 2)
            end_x = min(width, start_x + fov_width)
            end_y = min(height, start_y + fov_height)

            # Crop and resize
            cropped = self.input_image[start_y:end_y, start_x:end_x]
            resized_image = cv2.resize(cropped, (new_width, new_height), interpolation=interpolation)
        else:
            # Resize the entire image
            resized_image = cv2.resize(self.input_image, (new_width, new_height), interpolation=interpolation)

        # Update the output
        self.update_output(resized_image)

    def apply_resolution(self):
        if self.input_image is None:
            return

        # Get the resolution from the slider
        resolution = int(self.resolution_slider.get())

        # Get the selected interpolation method from the zoom type dropdown
        zoom_type = self.zoom_type_var.get()
        interpolation_methods = {
            "Nearest": cv2.INTER_NEAREST,
            "Linear": cv2.INTER_LINEAR,
            "Bilinear": cv2.INTER_CUBIC,  # Note: Bilinear is typically INTER_LINEAR
            "Bicubic": cv2.INTER_CUBIC,
            "Area": cv2.INTER_AREA
        }
        interpolation = interpolation_methods.get(zoom_type, cv2.INTER_LINEAR)

        # Resize the image to the specified resolution using the selected interpolation method
        resized_image = cv2.resize(self.input_image, (resolution, resolution), interpolation=interpolation)

        # Update the output
        self.update_output(resized_image)

    def apply_pixels(self):
        if self.input_image is None:
            return

        # Get the number of pixels per unit area from the slider
        pixels = int(self.pixels_slider.get())

        # Calculate the new dimensions based on the number of pixels
        height, width = self.input_image.shape
        new_width = int(width * (pixels / 100))
        new_height = int(height * (pixels / 100))

        # Resize the image to the new dimensions using INTER_NEAREST
        modified_image = cv2.resize(self.input_image, (new_width, new_height), interpolation=cv2.INTER_NEAREST)

        # Resize back to the original dimensions
        modified_image = cv2.resize(modified_image, (width, height))

        # Update the output
        self.update_output(modified_image)

    def apply_noise_denoise(self):
        if self.input_image is None:
            return

        # Get the source image based on the selected source
        source = self.source_var.get()
        if source == "Input":
            image = self.input_image.copy()
        elif source == "Output 1":
            image = self.output1_image.copy()
        elif source == "Output 2":
            image = self.output2_image.copy()
        else:
            return

        # Apply Noise
        noise_type = self.noise_var.get()
        if noise_type == "Gaussian":
            noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
            image = cv2.add(image, noise)
        elif noise_type == "Salt-and-Pepper":
            noise = np.random.random(image.shape)
            image[noise < 0.02] = 0
            image[noise > 0.98] = 255
        elif noise_type == "Speckle":
            noise = np.random.normal(0, 1, image.shape)
            image = np.clip(image * (1 + noise * 0.2), 0, 255).astype(np.uint8)

        # Apply Denoising
        denoise_type = self.denoise_var.get()
        if denoise_type == "Gaussian":
            image = cv2.GaussianBlur(image, (5, 5), 0)
        elif denoise_type == "Median":
            image = cv2.medianBlur(image, 5)
        elif denoise_type == "Bilateral":
            image = cv2.bilateralFilter(image, 9, 75, 75)

        # Update the output
        self.update_output(image)

    def apply_filter(self):
        if self.input_image is None:
            return

        # Get the source image based on the selected source
        source = self.source_var.get()
        if source == "Input":
            image = self.input_image.copy()
        elif source == "Output 1":
            image = self.output1_image.copy()
        elif source == "Output 2":
            image = self.output2_image.copy()
        else:
            return

        filter_type = self.filter_var.get()

        if filter_type == "Lowpass":
            image = cv2.GaussianBlur(image, (5, 5), 0)
        elif filter_type == "Highpass":
            lowpass = cv2.GaussianBlur(image, (5, 5), 0)
            highpass = cv2.subtract(image, lowpass)
            # Normalize the highpass result to avoid clipping
            highpass = cv2.normalize(highpass, None, 0, 255, cv2.NORM_MINMAX)
            image = highpass
        elif filter_type == "Sharpen":
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            image = cv2.filter2D(image, -1, kernel)
        elif filter_type == "Edge Detection":
            image = cv2.Canny(image, 100, 200)

        # Update the output
        self.update_output(image)

    def apply_contrast(self):
        if self.input_image is None:
            return

        # Get the source image based on the selected source
        source = self.source_var.get()
        if source == "Input":
            image = self.input_image.copy()
        elif source == "Output 1":
            image = self.output1_image.copy()
        elif source == "Output 2":
            image = self.output2_image.copy()
        else:
            return

        contrast_type = self.contrast_var.get()

        if contrast_type == "Histogram Equalization":
            image = cv2.equalizeHist(image)
        elif contrast_type == "CLAHE":
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            image = clahe.apply(image)
        elif contrast_type == "Gamma Correction":
            gamma = 1.5
            image = np.uint8(cv2.pow(image / 255.0, gamma) * 255)

        # Update the output
        self.update_output(image)

    def select_roi(self, roi_type):
        if self.input_image is None:
            return
        print(f"Select {roi_type} by drawing a rectangle on the input or output image.")
        self.current_roi_type = roi_type

    def start_draw_roi(self, event):
        self.drawing = True
        self.start_point = (event.x, event.y)
        canvas = event.widget
        if canvas == self.input_canvas:
            if self.rectangle_ids["input"]:
                self.input_canvas.delete(self.rectangle_ids["input"])
        elif canvas == self.output1_canvas:
            if self.rectangle_ids["output1"]:
                self.output1_canvas.delete(self.rectangle_ids["output1"])
        elif canvas == self.output2_canvas:
            if self.rectangle_ids["output2"]:
                self.output2_canvas.delete(self.rectangle_ids["output2"])

    def draw_roi(self, event):
        if self.drawing:
            canvas = event.widget
            if self.current_rectangle:
                canvas.delete(self.current_rectangle)
            self.current_rectangle = canvas.create_rectangle(
                self.start_point[0], self.start_point[1], event.x, event.y,
                outline="red", width=2
            )

    def end_draw_roi(self, event):
        if self.drawing:
            self.drawing = False
            self.end_point = (event.x, event.y)
            canvas = event.widget

            # Store the rectangle ID
            if canvas == self.input_canvas:
                self.rectangle_ids["input"] = self.current_rectangle
            elif canvas == self.output1_canvas:
                self.rectangle_ids["output1"] = self.current_rectangle
            elif canvas == self.output2_canvas:
                self.rectangle_ids["output2"] = self.current_rectangle

            # Scale ROI coordinates to match the original image size
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            if canvas == self.input_canvas:
                img_height, img_width = self.input_image.shape
            elif canvas == self.output1_canvas:
                img_height, img_width = self.output1_image.shape
            elif canvas == self.output2_canvas:
                img_height, img_width = self.output2_image.shape

            x1 = int(self.start_point[0] * img_width / canvas_width)
            y1 = int(self.start_point[1] * img_height / canvas_height)
            x2 = int(self.end_point[0] * img_width / canvas_width)
            y2 = int(self.end_point[1] * img_height / canvas_height)

            # Store ROI
            if canvas == self.input_canvas:
                image = self.input_image
            elif canvas == self.output1_canvas:
                image = self.output1_image
            elif canvas == self.output2_canvas:
                image = self.output2_image

            if self.current_roi_type == "roi1":
                self.roi1 = image[y1:y2, x1:x2]
                print("ROI 1 selected")
            elif self.current_roi_type == "roi2":
                self.roi2 = image[y1:y2, x1:x2]
                print("ROI 2 selected")
            elif self.current_roi_type == "noise_roi":
                self.noise_roi = image[y1:y2, x1:x2]
                print("Noise ROI selected")

    def calculate_snr(self):
        if self.roi1 is None or self.noise_roi is None:
            self.snr_label.config(text="SNR: Please select both ROI 1 and Noise ROI")
            return
        signal_mean = np.mean(self.roi1)
        noise_mean, noise_std = np.mean(self.noise_roi), np.std(self.noise_roi)
        if noise_std == 0:
            self.snr_label.config(text="SNR: Error (Noise std is zero)")
            return
        snr = abs(signal_mean - noise_mean) / noise_std
        self.snr_label.config(text=f"SNR: {snr:.2f}")

    def calculate_cnr(self):
        if self.roi1 is None or self.roi2 is None or self.noise_roi is None:
            self.cnr_label.config(text="CNR: Please select ROI 1, ROI 2, and Noise ROI")
            return
        signal1_mean = np.mean(self.roi1)
        signal2_mean = np.mean(self.roi2)
        _, noise_std = np.mean(self.noise_roi), np.std(self.noise_roi)
        if noise_std == 0:
            self.cnr_label.config(text="CNR: Error (Noise std is zero)")
            return
        cnr = abs(signal1_mean - signal2_mean) / noise_std
        self.cnr_label.config(text=f"CNR: {cnr:.2f}")

    def apply_brightness_contrast(self):
        if self.input_image is None:
            return

        # Get the source image based on the selected source
        source = self.source_var.get()
        if source == "Input":
            image = self.input_image.copy()
        elif source == "Output 1":
            image = self.output1_image.copy()
        elif source == "Output 2":
            image = self.output2_image.copy()
        else:
            return

        brightness = self.brightness_slider.get()
        contrast = self.contrast_slider.get()
        image = cv2.convertScaleAbs(image, alpha=1 + contrast / 100, beta=brightness)

        # Update the output
        self.update_output(image)

    def set_fov_center(self):
        print("Click on the input image to set the FOV center.")
        self.input_canvas.bind("<Button-1>", self.select_fov_center)

    def select_fov_center(self, event):
        self.fov_center = (event.x, event.y)
        self.input_canvas.unbind("<Button-1>")
        print(f"FOV center set at: {self.fov_center}")

    def apply_fov(self):
        if self.input_image is None or self.fov_center is None:
            return
        fov_size = self.fov_slider.get() / 100
        height, width = self.input_image.shape
        fov_width = int(width * fov_size)
        fov_height = int(height * fov_size)

        # Scale FOV center to image coordinates
        canvas_width = self.input_canvas.winfo_width()
        canvas_height = self.input_canvas.winfo_height()
        x = int(self.fov_center[0] * width / canvas_width)
        y = int(self.fov_center[1] * height / canvas_height)

        # Calculate crop boundaries
        start_x = max(0, x - fov_width // 2)
        start_y = max(0, y - fov_height // 2)
        end_x = min(width, start_x + fov_width)
        end_y = min(height, start_y + fov_height)

        # Crop and resize
        cropped = self.input_image[start_y:end_y, start_x:end_x]
        result = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_LINEAR)
        self.update_output(result)

    def update_output(self, image):
        if self.apply_to_var.get() == "Output 1":
            self.output1_image = image
            self.display_image(image, self.output1_canvas)
        else:
            self.output2_image = image
            self.display_image(image, self.output2_canvas)

    def undo(self):
        if self.output1_image is not None:
            self.output1_image = None
            self.display_image(self.input_image, self.output1_canvas)

    def reset(self):
        self.input_image = None
        self.output1_image = None
        self.output2_image = None
        self.input_canvas.delete("all")
        self.output1_canvas.delete("all")
        self.output2_canvas.delete("all")
        self.snr_label.config(text="SNR: N/A")
        self.cnr_label.config(text="CNR: N/A")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ImageViewer()
    app.run() 
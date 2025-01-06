# Organ Classification Using Deep Learning

This repository contains a deep learning model for classifying medical images into different organ categories (brain, breast, limb, and lung). The model is built using TensorFlow and Keras, and it is trained on a dataset of medical images.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Dataset](#dataset)
3. [Model Architecture](#model-architecture)
4. [Training](#training)
5. [Evaluation](#evaluation)
6. [Usage](#usage)
7. [Results](#results)
8. [Dependencies](#dependencies)
9. [License](#license)

---

## Project Overview

The goal of this project is to classify medical images into four categories:
- Brain
- Breast
- Limb
- Lung

The model is trained using a Convolutional Neural Network (CNN) implemented in TensorFlow and Keras. The trained model is saved as `organ_classification_model.h5`.

---

## Dataset

The dataset used for training and validation is organized into four folders, each corresponding to one of the organ categories. The dataset is split into training and validation sets.

- **Training Data**: Located in `/kaggle/input/dataset4/data-set/training`
- **Validation Data**: Located in `/kaggle/input/dataset4/data-set/validation`

Each folder contains images of the respective organ.

---

## Model Architecture

The model architecture is as follows:
- **Input Layer**: 150x150 RGB images
- **Convolutional Layers**:
  - Conv2D (32 filters, 3x3 kernel, ReLU activation)
  - MaxPooling2D
  - Conv2D (64 filters, 3x3 kernel, ReLU activation)
  - MaxPooling2D
- **Fully Connected Layers**:
  - Flatten
  - Dense (128 units, ReLU activation)
  - Dropout (0.5)
  - Dense (4 units, softmax activation) for classification

The model is compiled using the Adam optimizer and categorical cross-entropy loss.

---

## Training

The model was trained for 10 epochs with early stopping to prevent overfitting. The training process achieved a validation accuracy of **95%**.

### Training Parameters:
- **Batch Size**: 32
- **Image Size**: 150x150
- **Epochs**: 10
- **Early Stopping**: Patience of 3 epochs

---

## Evaluation

The model was evaluated on the validation dataset, achieving the following metrics:
- **Validation Accuracy**: 95%
- **Validation Loss**: 0.0855

---

## Usage

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/organ-classification.git
cd organ-classification
```

### 2. Install Dependencies
Make sure you have the required dependencies installed. You can install them using:
```bash
pip install -r requirements.txt
```

### 3. Load the Model
You can load the trained model using TensorFlow:
```python
from tensorflow.keras.models import load_model
model = load_model('organ_classification_model.h5')
```

### 4. Predict on New Images
Use the `predict_organ` function to classify a new image:
```python
from tensorflow.keras.preprocessing import image
import numpy as np

def predict_organ(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction)
    organs = ['brain', 'breast', 'limb', 'lung']
    return organs[predicted_class_index]

# Example usage
image_path = 'path_to_your_image.jpg'
predicted_class = predict_organ(image_path)
print(f"Predicted Organ: {predicted_class}")
```

---

## Results

The model achieved a high validation accuracy of **95%**, demonstrating its effectiveness in classifying medical images into the correct organ categories.

### Example Predictions:
- **Input Image**: `90-rotated1-rotated2-rotated3.jpg`
- **Predicted Class**: Limb
- **Probabilities**: [0.01, 0.02, 0.95, 0.02]

---

## Dependencies

The following Python libraries are required to run the code:
- TensorFlow
- Keras
- NumPy
- Matplotlib
- OpenCV

You can install them using:
```bash
pip install tensorflow numpy matplotlib opencv-python
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- The dataset used in this project was sourced from [Kaggle](https://www.kaggle.com).
- Special thanks to the TensorFlow and Keras teams for providing the tools to build this model.

---


# DICOM Medical Image Analyzer

A full-stack web application designed for processing, analyzing, and visualizing medical imaging data (DICOM format). This project was developed to demonstrate proficiency in medical software engineering, client-server architecture, and digital signal processing, with a user interface inspired by premium medical workstations like Siemens syngo.via.

## 🚀 Features

- **DICOM Parsing**: Extracts critical patient metadata (Name, Age, Sex, Modality, Study Date) directly from `.dcm` files using `pydicom`.
- **High-Quality Upscaling**: Utilizes OpenCV's Bicubic Interpolation (`cv2.INTER_CUBIC`) on the backend to elegantly scale low-resolution medical scans (like small MRI/CT samples) without pixelation.
- **Real-Time Image Processing**: Applies medical image filters on the fly:
  - **CLAHE** (Contrast Limited Adaptive Histogram Equalization) for enhancing local contrast in tissues.
  - **Sobel Edge Detection** for highlighting bone structures and boundaries.
  - **Inversion** for better visualization of specific pathologies.
- **Interactive Window/Level (W/L)**: Allows doctors/users to adjust the contrast and brightness (Window Width and Window Center) simply by clicking and dragging the mouse over the image canvas.
- **Mathematical Analytics**: Calculates and visualizes the exact pixel density distribution (tissue radiodensity) using a responsive bar chart powered by `Chart.js`.
- **Premium Dark UI**: A responsive, modern dark theme designed specifically to reduce eye strain in dimly lit radiological environments, featuring Siemens-inspired teal accents.

## 🛠️ Technology Stack

- **Backend**: Python 3.10, Flask
- **Medical Imaging**: `pydicom` (parsing), `OpenCV` (image processing & interpolation), `NumPy` (matrix calculations), `Pillow` (PNG encoding)
- **Frontend**: HTML5 Canvas, Vanilla JavaScript (ES6+), CSS3 (CSS Grid/Flexbox)
- **Analytics**: `Chart.js`

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Mamaxa2512/dicom-analyzer.git
   cd dicom-analyzer
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # venv\Scripts\activate   # On Windows
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running the Application

1. Start the Flask development server:
   ```bash
   python run.py
   ```
2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```
3. Upload a `.dcm` file from the `sample_dicoms` directory to explore the features.

## ⚠️ Disclaimer
**For Educational Purposes Only.** This software is a student project and is *not* FDA-approved or CE-marked for clinical diagnostic use. It should not be used to make medical decisions.

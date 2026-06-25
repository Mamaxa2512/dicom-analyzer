# 🏥 DICOM Medical Image Analyzer

A web-based medical imaging workstation built with Python and Flask, featuring real-time image processing filters and **AI-powered radiological analysis** via Google Gemini.

Built as a portfolio project demonstrating expertise in medical imaging, computer vision, and AI integration — core competencies for healthcare technology companies like Siemens Healthineers.

---

## ✨ Features

| Feature | Technology |
|---|---|
| DICOM file parsing & metadata extraction | `pydicom` |
| Medical image rendering | HTML5 Canvas |
| Image filters (CLAHE, Invert, Edge Detection) | OpenCV |
| High-quality image upscaling | `cv2.INTER_CUBIC` |
| Pixel intensity histogram | Chart.js |
| **AI Radiological Analysis** | **Google Gemini 2.5 Flash** |
| Markdown report rendering | marked.js |
| Premium dark UI (Siemens syngo.via inspired) | CSS |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- A [Google AI Studio](https://aistudio.google.com/) API key

### Installation

```bash
# Clone the repository
git clone https://github.com/Mamaxa2512/dicom-analyzer.git
cd dicom-analyzer

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

### Run

```bash
python run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 📂 Project Structure

```
dicom-analyzer/
├── app/
│   ├── __init__.py            # Flask app factory
│   ├── routes.py              # API endpoints & routing
│   ├── dicom_parser.py        # DICOM metadata & pixel extraction
│   └── image_processor.py     # OpenCV image filters & upscaling
├── static/
│   ├── css/style.css          # Premium dark medical theme
│   ├── js/viewer.js           # Canvas rendering & AI integration
│   └── uploads/               # Uploaded DICOM files
├── templates/
│   ├── base.html              # Base layout template
│   ├── index.html             # File upload page
│   └── viewer.html            # Image viewer & analysis page
├── sample_dicoms/             # Demo DICOM files
├── requirements.txt
├── run.py                     # Application entry point
└── .env                       # API key (not tracked by git)
```

---

## 🔬 How It Works

1. **Upload** a `.dcm` file through the web interface
2. **View** the medical image with patient metadata displayed alongside
3. **Apply filters** — CLAHE contrast enhancement, edge detection, or color inversion
4. **Run AI Analysis** — sends the image to Google Gemini for automated radiological reporting
5. **Read the report** — structured findings including study type, anatomical findings, detected anomalies, differential diagnosis, and a medical disclaimer

---

## 🛡️ Security

- API keys are stored in `.env` and excluded from version control via `.gitignore`
- All AI-generated reports include a mandatory medical disclaimer
- No patient data is stored permanently or transmitted to third parties beyond the AI analysis request

---

## ⚠️ Disclaimer

This application is a **student portfolio project** and is intended for educational and demonstration purposes only. AI-generated reports are **not** a substitute for professional medical diagnosis. Do not use this tool for clinical decision-making.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

"""
Flask routes for the application.
"""
from PIL import Image
from app.dicom_parser import parse_dicom, get_image_as_png, get_pixel_array

# pyrefly: ignore [missing-import]
from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_file, jsonify
import os
import io
from app import image_processor
from dotenv import load_dotenv
import google.generativeai as genai

main_bp = Blueprint("main", __name__)

@main_bp.route("/api/report/<file_id>")
def generate_report(file_id):
    load_dotenv()
    api = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key = api)
    model = genai.GenerativeModel('gemini-2.5-flash')
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file_id)
    photo = get_image_as_png(filepath)

    indtuction = """Role: You are a highly qualified diagnostic physician (radiologist/pathologist) with years of experience in analyzing medical images. Your task is to objectively, thoroughly, and professionally analyze the provided image.

Instructions:

    Carefully examine the image and determine its modality (e.g., X-ray, MRI, CT scan, Ultrasound, macroscopic image, or histology).

    Describe the visible anatomical structures.

    Pay special attention to any deviations from the norm, anomalies, artifacts, or signs of pathology.

    Use precise medical terminology and maintain an objective tone. Do not provide definitive clinical diagnoses; instead, describe the visual/radiological findings and suggest probable differential conditions.

Response Format:
Structure your response clearly using the following sections:

    Type of Study: [Specify the modality, projection, and body part]

    Quality Assessment: [Assess whether the image quality, contrast, and resolution are adequate for comprehensive analysis]

    Anatomical Findings (Normal): [Describe structures that appear unremarkable/normal]

    Detected Anomalies/Pathologies: [Detail any suspicious areas: their size, shape, density/signal intensity, margins, and localization]

    Impression: [Provide a concise summary of the findings and a differential diagnosis]

    Medical Disclaimer: [Mandatory warning stating that this analysis is AI-generated, does not substitute professional medical advice, and must not be used for definitive diagnosis or self-treatment]."""
    result = model.generate_content([indtuction, photo])
    return jsonify({"report":result.text})


    


@main_bp.route("/")
def index():
    
    return render_template("index.html")

@main_bp.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], f.filename)
    f.save(save_path)
    return redirect(url_for("main.viewer", file_id=f.filename))


@main_bp.route("/viewer/<file_id>")
def viewer(file_id):
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file_id)
    dicom_data = parse_dicom(filepath)
    return render_template("viewer.html", file_id = file_id, dicom_data = dicom_data)


@main_bp.route("/api/process/<file_id>", methods=["POST"])
def process(file_id):
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], file_id)
    json = request.json or {}
    type = json.get("filter", "original")
    img = get_pixel_array(filepath)
    if type == "original":
        image = get_image_as_png(filepath)
    else:
        if type == "window":
            window = float(json.get("window", 0))
            level = float(json.get("level", 0))
            img = image_processor.apply_window_level(img, window, level)
        elif type == "clahe":
            img = image_processor.apply_clahe(img)
        elif type == "edge":
            img = image_processor.apply_edge_detection(img)
        elif type == "invert":
            img = image_processor.apply_invert(img)

        img = image_processor.upscale_for_display(img)
        image = Image.fromarray(img)
    
    memory_file = io.BytesIO()
    image.save(memory_file, "PNG")
    memory_file.seek(0)
    
    
    return send_file(memory_file, mimetype='image/png')










@main_bp.route("/api/download/<file_id>")
def download(file_id):
    img = get_image_as_png(os.path.join(current_app.config["UPLOAD_FOLDER"], file_id))
    memory_file = io.BytesIO()
    img.save(memory_file, "PNG")
    memory_file.seek(0)
    return send_file(memory_file, mimetype='image/png')



@main_bp.route("/api/histogram/<file_id>")
def histogram(file_id):
    arr = get_pixel_array(os.path.join(current_app.config["UPLOAD_FOLDER"], file_id))
    hist =  image_processor.get_histogram(arr)
    return jsonify({"histogram": hist})


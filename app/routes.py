"""
Flask routes for the application.
"""
from PIL import Image
from app.dicom_parser import parse_dicom, get_image_as_png, get_pixel_array

# pyrefly: ignore [missing-import]
from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_file
import os
import io
from app import image_processor


main_bp = Blueprint("main", __name__)

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


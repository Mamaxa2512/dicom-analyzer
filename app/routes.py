"""
Flask routes for the application.
"""
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    # TODO: Phase 1 - Render index.html
    return render_template("index.html")

@main_bp.route("/upload", methods=["POST"])
def upload():
    # TODO: Phase 1 - Handle file upload and parsing
    pass

@main_bp.route("/viewer/<file_id>")
def viewer(file_id):
    # TODO: Phase 1 - Render viewer.html
    pass

@main_bp.route("/api/process/<file_id>", methods=["POST"])
def process(file_id):
    # TODO: Phase 2 - Handle image processing filters
    pass

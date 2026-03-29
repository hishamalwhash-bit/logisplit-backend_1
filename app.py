from flask import Flask, request, send_file
import os
from werkzeug.utils import secure_filename
from zipfile import ZipFile

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return """
    <h2>LogiSplit AI - Production System</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="files" multiple>
        <button type="submit">Upload & Process</button>
    </form>
    """

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")

    saved_files = []

    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        saved_files.append(path)

    zip_path = os.path.join(OUTPUT_FOLDER, "result.zip")

    with ZipFile(zip_path, "w") as zipf:
        for f in saved_files:
            zipf.write(f, os.path.basename(f))

    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run()

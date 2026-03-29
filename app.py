from flask import Flask, request, send_file
import os
import re
from werkzeug.utils import secure_filename
from zipfile import ZipFile
from PIL import Image
import pytesseract

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_shipment(text):
    match = re.search(r'70\d{5,}', text)
    return match.group(0) if match else "UNKNOWN"

@app.route("/")
def home():
    return """
    <h2>LogiSplit AI - FINAL SYSTEM</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="files" multiple>
        <button type="submit">Upload & Process</button>
    </form>
    """

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")

    zip_path = os.path.join(OUTPUT_FOLDER, "result.zip")

    with ZipFile(zip_path, "w") as zipf:
        for file in files:
            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)

            try:
                image = Image.open(path)
                text = pytesseract.image_to_string(image)
                shipment = extract_shipment(text)
            except:
                shipment = "UNKNOWN"

            new_name = f"{shipment}.jpg"
            new_path = os.path.join(UPLOAD_FOLDER, new_name)

            os.rename(path, new_path)
            zipf.write(new_path, new_name)

    return send_file(zip_path, as_attachment=True)

import os
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))

from flask import Flask, render_template, request
import qrcode
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Folder to save QR code images
QR_FOLDER = "static/qr_codes"
os.makedirs(QR_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_filename = None  # This will store the filename for the generated QR

    if request.method == "POST":
        data = request.form.get("data")  # Get text or URL from form
        if data:
            # 1️⃣ Create QR object
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4
            )

            # 2️⃣ Add data and make image
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # 3️⃣ Save image file
            qr_filename = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            qr_path = os.path.join(QR_FOLDER, qr_filename)
            img.save(qr_path)

    return render_template("index.html", qr_filename=qr_filename)

if __name__ == "__main__":
    app.run(debug=True)

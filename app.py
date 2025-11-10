from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    img_data = None  # placeholder for QR code

    if request.method == 'POST':
        data = request.form.get('data')
        fill_color = request.form.get('fill_color', 'black')
        back_color = request.form.get('back_color', 'white')
        box_size = int(request.form.get('size', 10))
        error_level = request.form.get('error', 'M')

        error_correction = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }[error_level]

        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction,
            box_size=box_size,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        # Convert image to base64 string to embed in HTML
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        img_data = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render_template('index.html', img_data=img_data)

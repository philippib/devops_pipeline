from flask import Flask, render_template, request, send_file, url_for
import qrcode
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/')
def index():
    qr_code_url = request.args.get('qr_code_url')
    return render_template('index.html', qr_code_url=qr_code_url)

@app.route('/generate_qr')
def generate_qr():
    data = request.args.get('data')
    if not data:
        return render_template('index.html')

    qr = qrcode.make(data)
    img_io = BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)

    tmp_file_path = os.path.join('/tmp', 'qrcode.png')
    
    with open(tmp_file_path, 'wb') as f:
        f.write(img_io.getvalue())

    qr_code_url = url_for('serve_qr_code', _external=True)
    return render_template('index.html', qr_code_url=qr_code_url)

@app.route('/qr_code')
def serve_qr_code():
    tmp_file_path = os.path.join('/tmp', 'qrcode.png')
    return send_file(tmp_file_path, mimetype='image/png')

@app.route('/download_qr')
def download_qr_code():
    tmp_file_path = os.path.join('/tmp', 'qrcode.png')
    return send_file(tmp_file_path, as_attachment=True, download_name='qrcode.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
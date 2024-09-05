from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr')
def generate_qr():
    data = request.args.get('data')
    if not data:
        return render_template('index.html')

    qr = qrcode.make(data)
    img_io = BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    
    qr_code_url = '/static/qrcode.png'
    
    with open('static/qrcode.png', 'wb') as f:
        f.write(img_io.getvalue())
    
    return render_template('index.html', qr_code_url=qr_code_url)

if __name__ == '__main__':
    app.run(debug=True)
import os
from flask import Flask, render_template, request, send_from_directory
from PIL import Image
from fpdf import FPDF

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DOWNLOAD_FOLDER = 'downloads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/imgtopdf')
def imgtopdf():
    return render_template('imgtopdf.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    else:
        return 'Invalid file'

@app.route('/convert/<filename>')
def convert(filename):
    if allowed_file(filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image = Image.open(filepath)
        if image.width > image.height:
            image = image.rotate(90, expand=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.image(filepath, 0, 0, pdf.w, pdf.h)
        pdf_filename = os.path.splitext(filename)[0] + '.pdf'
        pdf_filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], pdf_filename)
        pdf.output(pdf_filepath, 'F')
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], pdf_filename, as_attachment=True)
    else:
        return 'Invalid file'

if __name__ == '__main__':
    app.run()

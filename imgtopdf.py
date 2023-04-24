import os
from PIL import Image
from fpdf import FPDF

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_pdf(filepath):
    if allowed_file(filepath):
        image = Image.open(filepath)
        if image.width > image.height:
            image = image.rotate(90, expand=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.image(filepath, 0, 0, pdf.w, pdf.h)
        pdf_filename = os.path.splitext(os.path.basename(filepath))[0] + '.pdf'
        pdf_filepath = os.path.join(DOWNLOAD_FOLDER, pdf_filename)
        pdf.output(pdf_filepath, 'F')
        return pdf_filename
    else:
        return None

if __name__ == '__main__':
    filepath = input("Enter the filepath of the image to be converted to PDF: ")
    convert_to_pdf(filepath)

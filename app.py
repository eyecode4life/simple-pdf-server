
from flask import Flask, send_from_directory, render_template_string, send_file
import os
import fitz  # PyMuPDF
from PIL import Image

app = Flask(__name__)

# Directory where your PDF files are stored
PDF_DIR = 'pdfs'
COVERS_DIR = 'pdfs/covers'

@app.route('/')
def list_books():
    # List all PDF files in the directory
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]

    # Create a simple HTML template to display the list of books and covers
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>PDF Books</title>
        <style>
            .book {
                margin-bottom: 20px;
                display: flex;
                align-items: center;
            }
            img {
                width: 150px;
                height: auto;
                margin-right: 20px;
            }
            a {
                text-decoration: none;
                color: #3498db;
            }
        </style>
    </head>
    <body>
        <h1>Available PDF Books:</h1>
        <ul>
            {% for pdf_file in pdf_files %}
                <div class="book">

                    <img src="/covers/{{ pdf_file.replace('.pdf', '.jpg') }}" alt="Cover of {{ pdf_file }}">
                    <a href="/{{ pdf_file }}">{{ pdf_file }}</a>
                </div>
            {% endfor %}
        </ul>
    </body>
    </html>
    '''
    
    #<img src="{{ url_for('get_pdf_thumbnail', filename=pdf_file) }}" alt="Cover of {{ pdf_file }}">
    # Render the template with the list of PDF files
    return render_template_string(html_template, pdf_files=pdf_files)

@app.route('/<path:filename>')
def download_file(filename):
    if filename.endswith('.pdf'):
        return send_from_directory(PDF_DIR, filename)
    else:
        return "Invalid file type", 403

def create_thumbnail(filename):
    pdf_path = os.path.join(PDF_DIR, filename)
    # Load the PDF and extract the first page
    pdf_document = fitz.open(pdf_path)
    first_page = pdf_document.load_page(0)  # Page numbers start at 0
    # Render the first page as an image
    pix = first_page.get_pixmap()
    thumbnail_path = os.path.join(COVERS_DIR, f"{filename.replace('.pdf', '.jpg')}")
    # Save the image to a temporary file
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    image.save(thumbnail_path)
    return thumbnail_path


@app.route('/covers/<path:filename>')
def get_pdf_cover(filename):
    cover_path = os.path.join(COVERS_DIR, filename)
    if(os.path.exists(cover_path)) :
        return send_file(cover_path, mimetype='image/jpg')
    else:
        pdf_file = filename.replace('.jpg','.pdf')
        created_file = create_thumbnail(pdf_file)
        return send_file(created_file, mimetype='image/jpg')

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', debug=True)



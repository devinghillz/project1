"""

from flask import Flask, render_template, request
from flask import send_file
import os
import re
import openpyxl
from googletrans import Translator

app = Flask(__name__)

@app.route('/')
def index():
    # Initial upload page
    return render_template('upload.html')

@app.route("/upload", methods=["POST"])
def upload():
    # traslation + upload(server) + masking
    file = request.files["file"]
    file.save(os.path.join("uploads", file.filename))
    
    workbook = openpyxl.load_workbook(os.path.join("uploads", file.filename))
    sheet = workbook.active

    translator = Translator()
    for row in sheet.iter_rows():
        for cell in row:
            # change 'dest' option
            translated_text = translator.translate(cell.value, dest='en').text
            # masking RRN
            translated_text = re.sub(r'(\d{6})[-]\d{7}', r'\1-*******', translated_text)
            # masking e-mail
            translated_text = re.sub(r'[\w\.-]+@[\w\.-]+', r'\w{1}***@***.***', translated_text)
            cell.value = translated_text

    workbook.save(f'[translated]{file.filename}.xlsx')
    
    # upload result page
    return render_template('.html', file_name=file.filename)

@app.route("/download")
def download():
    return ""
    
if __name__ == '__main__':
    app.run(debug=True)

"""
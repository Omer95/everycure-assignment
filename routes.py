from flask import Flask, request
from io import BytesIO
from pdfminer_utils import process_document

app = Flask(__name__)

@app.route('/api/v1/extract', methods=['POST'])
def extract():
    if request.files['file']:
        file = request.files['file']
        filedata = BytesIO(file.read())
        pages = process_document(filedata, [0,1])
        print(pages[1])
        return 'file found', 200
    else:
        return 'file not attached', 400
    

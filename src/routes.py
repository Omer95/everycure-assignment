from flask import Flask, request
from io import BytesIO
from pdfminer_utils import process_document
from inference import extract_entities
from utils import prepare_response, allowed_file, write_results_to_disk
from utils import config
from database_entry import write_results_to_database
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

@app.route('/api/v1/extract', methods=['POST'])
def extract():
    if len(request.files) > 1:
        return 'Please upload one file.', 500
    if request.files['file']:
        file = request.files['file']
        filename = secure_filename(file.filename)
        if allowed_file(file.filename) == False:
            return 'Unsupported file type.', 415
        filedata = BytesIO(file.read())
        pages = process_document(filedata, [0,1])
        entities = []
        for page in pages:
            entities += extract_entities(pages[page])
        results_dir = '{}_{}.txt'.format(filename.split('.')[0], str(uuid.uuid4()))
        write_results_to_disk(results_dir, entities)
        write_results_to_database(filename, results_dir)
        response = prepare_response(entities, pages[page])
        return response, 200
    else:
        return 'Bad request, file not included or empty filename.', 400

if '__main__' == __name__:
    app.run(host=config['SERVER']['HOST'], port=config['SERVER']['PORT'])
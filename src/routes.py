from flask import Flask, request
from io import BytesIO
from pdfminer_utils import process_document
from inference import extract_entities
from utils import prepare_response, allowed_file, write_results_to_disk
from utils import config
from database_entry import write_results_to_database
from werkzeug.utils import secure_filename
import uuid
import logging

app = Flask(__name__)
logging.basicConfig(filename=config['LOGFILE'], filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

@app.route('/api/v1/extract', methods=['POST'])
def extract():
    if len(request.files) > 1:
        logger.error('Multiple files sent to server. Aborting.')
        return 'Please upload one file.', 500
    
    if request.files['file']:
        file = request.files['file']
        filename = secure_filename(file.filename)

        if allowed_file(file.filename) == False:
            logger.error('Unsupported file type uploaded to server. Aborting.')
            return 'Unsupported file type.', 415
        
        filedata = BytesIO(file.read())

        logger.info('PDF document {} being parsed'.format(filename))
        pages = process_document(filedata, [0,1])
        entities = []

        logger.info('Entities being extracted from PDF document {}'.format(filename))
        for page in pages:
            entities += extract_entities(pages[page])

        results_dir = '{}_{}.txt'.format(filename.split('.')[0], str(uuid.uuid4()))
        logger.info('Writing entity results file {} to disk'.format(results_dir))
        write_results_to_disk(results_dir, entities)

        logger.info('Inserting entity record to inference table')
        write_results_to_database(filename, results_dir)

        response = prepare_response(entities, pages[page])
        return response, 200
    else:
        logger.error('No file included in HTTP request. Aborting.')
        return 'Bad request, file not included or empty filename.', 400

if '__main__' == __name__:
    app.run(host=config['SERVER']['HOST'], port=config['SERVER']['PORT'])
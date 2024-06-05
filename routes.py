from flask import Flask, request
from io import BytesIO
from pdfminer_utils import process_document
from inference import extract_entities

app = Flask(__name__)

@app.route('/api/v1/extract', methods=['POST'])
def extract():
    if request.files['file']:
        file = request.files['file']
        filedata = BytesIO(file.read())
        pages = process_document(filedata, [0,1])
        entities = []
        for page in pages:
            entities += extract_entities(pages[page])
        response = prepare_response(entities, pages[page])
        return response, 200
    else:
        return 'file not attached', 400
    
def prepare_response(entities, text):
    prepared_entities = []
    for entity in entities:
        prepared_entity = {'entity': entity['word'], 'start': entity['start'], 'end': entity['end']}
        context_start = entity['start'] - 70 if entity['start'] - 70 >= 0 else 0
        context_end = entity['end'] + 70 if entity['end'] + 70 < len(text) else len(text)
        prepared_entity['context'] = text[context_start:context_end]

        prepared_entities.append(prepared_entity)
    return prepared_entities

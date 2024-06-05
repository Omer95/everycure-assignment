import yaml
import os
import logging

with open('config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

stride = config['CONTEXT_STRIDE']

def prepare_response(entities, text):
    prepared_entities = []
    for entity in entities:
        prepared_entity = {'entity': entity['word'], 'start': entity['start'], 'end': entity['end']}
        context_start = entity['start'] - stride if entity['start'] - stride >= 0 else 0
        context_end = entity['end'] + stride if entity['end'] + stride < len(text) else len(text)
        prepared_entity['context'] = text[context_start:context_end]

        prepared_entities.append(prepared_entity)
    return prepared_entities

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'pdf'

def write_results_to_disk(filename, results):
    if not os.path.exists('data'):
        logging.info('creating data directory')
        os.mkdir('data')
    with open('/entity-extraction/data/{}'.format(filename), 'w') as writefile:
        writefile.write(str(results))
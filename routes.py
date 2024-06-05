from flask import Flask, request

app = Flask(__name__)

@app.route('/api/v1/extract', methods=['POST'])
def extract():
    if request.files['file']:
        return 'file found', 200
    else:
        return 'file not attached', 400
    

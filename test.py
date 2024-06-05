from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def hello():
    return 'Hello world', 200

if '__main__' == __name__:
    app.run(host='0.0.0.0')
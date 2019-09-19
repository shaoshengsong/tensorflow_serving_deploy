from flask import Flask

PATH_TO_LABELS = './data/labels.pbtxt'
SERVER_URL = 'http://localhost:8501/v1/models/faster_rcnn_resnet:predict'
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['PATH_TO_LABELS'] = PATH_TO_LABELS
app.config['SERVER_URL'] = SERVER_URL
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

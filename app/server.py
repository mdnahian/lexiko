from flask import Flask, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import string
import random

UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def generateRandom():
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))


@app.route('/')
def index():
	return 'server running...'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':

		if 'file' not in request.files:
			print 'bad'
			return '{ "error": "invalid request parameter" }'
        
        image_file = request.files['file']

        if image_file.filename == '':
        	print 'bad'
        	return '{ "error": "file not found" }'

       	if image_file and allowed_file(image_file.filename):
       		filename = secure_filename(image_file.filename)
       		image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       		print 'good'
       		return '{ "url": "' + url_for('uploaded_file', filename=filename) + '" }'
	
	else:
		return '{ "error": "invalid request method" }'



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)


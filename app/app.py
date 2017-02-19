from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit
from PIL import Image
from pytesseract import image_to_string
import string
import random
import io
import httplib, urllib, base64
import json

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'lexiko'
socketio = SocketIO(app)


BASE_URL = 'http://6862a278.ngrok.io'






def image_to_text(url):

	headers = {
	    # Request headers
	    'Content-Type': 'application/json',
	    'Ocp-Apim-Subscription-Key': 'be6d561231ec489d8593ca3ef59a67ba',
	}

	params = urllib.urlencode({
	    # Request parameters
	    'language': 'unk',
	    'detectOrientation ': 'true',
	})

	try:
	    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
	    conn.request("POST", "/vision/v1.0/ocr?%s" % params, '{ "url":"'+url+'" }', headers)
	    response = conn.getresponse()
	    data = response.read()
	    print data 
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))






	headers = {
	    # Request headers
	    'Content-Type': 'application/json',
	    'Ocp-Apim-Subscription-Key': 'be6d561231ec489d8593ca3ef59a67ba',
	}

	params = urllib.urlencode({
	    # Request parameters
	    'language': 'unk',
	    'detectOrientation ': 'true',
	})

	try:
	    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
	    conn.request("POST", "/vision/v1.0/ocr?%s" % params, '{ "url": "'+url+'" }', headers)
	    response = conn.getresponse()
	    raw = response.read()
	    data = json.loads(raw)

	    print 'got response'

	    print data
	except Exception as e:
		print 'Failed'
		print e







@app.route('/test')
def test():
	return render_template('test.html')



@socketio.on('image_sent')
def image_sent(raw):
	fileName = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(0, 6))

	img = Image.open(io.BytesIO(raw))
	img.save('static/img/'+fileName+'.jpg')

	imgg = BASE_URL+'/img/'+fileName+'.jpg'

	image_to_text(imgg)




@app.route('/<path:path>')
def sound_file(path):
    return url_for('static', filename=path)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(80))
	
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit
from PIL import Image
from pytesseract import image_to_string
import string
import random
import io
import httplib, urllib, base64
import json
import re
from  webMD import *

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'lexiko'
socketio = SocketIO(app)


BASE_URL = 'http://ec2-174-129-79-187.compute-1.amazonaws.com'	
	



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
	    conn.close()
	    return data
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))
	    return ''



@app.route('/test')
def test():
	return render_template('test.html')



@socketio.on('image_sent')
def image_sent(raw):
	fileName = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(0, 6))

	img = Image.open(io.BytesIO(raw))
	img.save('static/img/'+fileName+'.jpg')

	imgg = BASE_URL+'/img/'+fileName+'.jpg'

	raw_text = image_to_text(imgg)
		

	if raw_text != '':
		
		data = json.loads(raw_text)
		
		regions = data['regions']
	    	for region in regions:
	    		for line in region['lines']:
				for word in line['words']:
					text = ''.join(i for i in word['text'] if not i.isdigit())
					text = re.sub('\W+', ' ', text)

					if len(text) >= 5:
						print text
						response = text #search_web_md(text)
						
						if response != '':
							emit('response', '{ "name":"something" }')
							break

		return ''						
		
	else:
		print 'could not find any text in image'
	



@app.route('/<path:path>')
def sound_file(path):
    return url_for('static', filename=path)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(80), debug=True)
	

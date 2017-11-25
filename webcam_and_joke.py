import numpy
import cv2

import cognitive_face as CF
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json

import time

import json
import requests
import text_to_speech


##################################
# Configuration
##################################

# Path to folder with images
folder = 'file/'
# Time delay between frames in seconds
delay = 5.0


KEY = 'bb72da8595ab4d56a05a1d666f7933f6'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

uri_base = 'https://westcentralus.api.cognitive.microsoft.com'

# Request headers.
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': KEY,
}
# Request parameters.
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}


#################################
# Webcam code
#################################

emotions = ['not happy'] * 20

cam = cv2.VideoCapture(0)

count = 0
while(1):
	ret, frame = cam.read()
	frame_num = "%08d" % (count,)

	pathToFile = folder + frame_num + '.jpg'
	cv2.imwrite(pathToFile, frame)



	# Load raw image file into memory
	with open(pathToFile, 'rb' ) as f:
	    data = f.read()


	try:
	    # Execute the REST API call and get the response.
	    response = requests.request('POST', uri_base + '/face/v1.0/detect', json=None, data=data, headers=headers, params=params)

	    print ('Response:')
	    parsed = json.loads(response.text)
	    print (json.dumps(parsed, sort_keys=True, indent=2))

	except Exception as e:
	    print('Error:')
	    print(e)

	if response.text != '[]':

		json_response = response.json()
		mood = json_response[0]["faceAttributes"]["emotion"]


		if float(mood["happiness"]) > 0.5:
			emotions.append("happy")
		else:
			emotions.append("not happy")


		print(emotions[-10:-1])

		if "happy" not in emotions[-4:-1]:
			print("Looks like you need a joke. Here's one:")
			content = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
			parsed = json.loads(content.text)
			joke = parsed["joke"]
			print(joke)
			text_to_speech.speak("Here's a joke for you", 10000)
			text_to_speech.speak(joke, 8000)

	k = cv2.waitKey(1)
	count = count + 1
	time.sleep(delay)

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()
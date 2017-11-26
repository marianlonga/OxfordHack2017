import numpy
import cv2

import cognitive_face as CF
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json

import time

import json
import requests
import text_to_speech
import jokes
import tweet
import openurl
from PIL import Image


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


method_to_make_you_happier_count = 0

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

	    #print ('Response:')
	    parsed = json.loads(response.text)
	    #print (json.dumps(parsed, sort_keys=True, indent=2))

	except Exception as e:
	    print('Error:')
	    print(e)

	if str(parsed) != "[]":

		json_response = response.json()
		print(json_response)
		mood = json_response[0]["faceAttributes"]["emotion"]


		if float(mood["happiness"]) > 0.3:
			emotions.append("happy")
		else:
			emotions.append("not happy")


		#print(emotions[-10:-1])

		if "happy" not in emotions[-4:-1]:

			#print(method_to_make_you_happier_count)

			if method_to_make_you_happier_count == 0:
				## TELL A JOKE

				#print("Looks like you need a joke. Here's one:")
				#content = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
				#parsed = json.loads(content.text)
				#joke = parsed["joke"]
				joke = jokes.get_joke()
				#print(joke)

				#text_to_speech.speak("You look unhappy, here's a joke for you. " + joke, 8000)

				print("We have told you a joke!")

			if method_to_make_you_happier_count == 1:
				## CROP PICTURE TO YOUR FACE ONLY AND TWEET IT

				height = frame.shape[0]
				#print(height)
				width = frame.shape[1]
				#print(width)
				x1 = json_response[0]["faceRectangle"]["left"] - 70
				x2 = x1 + 70 + json_response[0]["faceRectangle"]["width"] + 70
				y1 = json_response[0]["faceRectangle"]["top"] - 150
				y2 = y1 + 150 + json_response[0]["faceRectangle"]["height"] + 70
				x1 = x1 if x1 > 0 else 0
				y1 = y1 if y1 > 0 else 0
				x2 = x2 if x2 < width else width - 1
				y2 = y2 if y2 < height else height - 1
				#print(x1, x2, y1, y2)

				cropped_frame = frame[y1:y2, x1:x2]
				cropped_frame_image = Image.fromarray(cropped_frame)
				cropped_frame_image.save('crop.png')

				#tweet.tweet("sad", cropped_frame)
				#cv2.imshow("cropped", cropped_frame)
				#cv2.waitKey(0)

				#tweet.tweet("I'm feeling " + str((json_response[0]["faceAttributes"]["emotion"]["sadness"])*100) + "% sad :(", 'crop.png')

				print("We have tweeted to get you help!")

			if method_to_make_you_happier_count == 2:
				## PLAY CAT VIDEO

				#openurl.play_cat_video()

				print("We have played a funny cat video!")

			method_to_make_you_happier_count = (method_to_make_you_happier_count + 1) % 3

		else:

			print("You're happy!")

#	k = cv2.waitKey(1)
#	count = count + 1
#	time.sleep(delay)

## When everything done, release the capture
#cam.release()
#cv2.destroyAllWindows()
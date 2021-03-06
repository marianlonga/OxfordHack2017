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
import json
import sys


##################################
# Configuration
##################################

# Path to folder with images
folder = 'file/'
# Time delay between frames in seconds
delay = 5.0


KEY = '1bae8b75b79a4a29bc8a30624aac17bc'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

BASE_URL = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

#uri_base = 'https://api.projectoxford.ai/emotion/v1.0/recognize'


# Request headers.
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': KEY,
}
# Request parameters.
params = "{}"
#params = {
#    'returnFaceId': 'true',
#    'returnFaceLandmarks': 'false',
#    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
#}


# clean



emotions = ['not happy'] * 20

cam = cv2.VideoCapture(0)


method_to_make_you_happier_count = 0

last_method_to_increase_happiness = "joke"
latest_joke_number = 0
just_told_a_joke = False

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
		response = requests.request('POST', "https://api.projectoxford.ai/emotion/v1.0/recognize", json=None, data=data, headers=headers, params=params)
		#print(response)
		#print ('Response:')
		parsed = json.loads(response.text)
		#print(parsed)
		#print (json.dumps(parsed, sort_keys=True, indent=2))
		#sys.exit()

	except Exception as e:
		print('Error:')
		print(e)

	if parsed != None and str(parsed) != "[]":

		# Check if last method to increase happiness was successful in making a person happy and if so,
		# increase score for corresponding method in JSON file
		if (emotions[-2] == "sad" and emotions[-1] == "happy"):
			with open('scores.json') as json_data:
				d = json.load(json_data)
				d[last_method_to_increase_happiness] = d[last_method_to_increase_happiness] + 1
			with open('scores.json', 'w') as outfile:
				json.dump(d, outfile)


		# # get current emotion
		# json_response = response.json()
		# # print(json_response)
		# mood = json_response[0]["faceAttributes"]["emotion"]
		# if float(mood["happiness"]) > 0.3:
		# 	emotions.append("happy")
		# else:
		# 	emotions.append("sad")

		happiness_level = float(parsed[0]['scores']['happiness'])
		print("Happiness: " + str(happiness_level))
		if happiness_level > 0.3:
			emotions.append("happy")
		else:
			emotions.append("sad")

		# if just told a joke, record its corresponding happiness value to JSON file
		if(just_told_a_joke):
			with open('jokes_scores.json') as json_data:
				d = json.load(json_data)
				d["joke" + str(latest_joke_number)] = d["joke" + str(latest_joke_number)] + happiness_level
			with open('jokes_scores.json', 'w') as outfile:
				json.dump(d, outfile)



		#print(emotions[-10:-1])

		just_told_a_joke = False

		# if you've been sad for the past 4 time stamps:
		if "happy" not in emotions[-4:-1]:

			#print(method_to_make_you_happier_count)

			if method_to_make_you_happier_count == 0:
				## TELL A JOKE

				#print("Looks like you need a joke. Here's one:")
				#content = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
				#parsed = json.loads(content.text)
				#joke = parsed["joke"]
				joke, joke_number = jokes.get_joke()
				latest_joke_number = joke_number
				#print(joke, joke_number)
				#print(joke)

				text_to_speech.speak("You look unhappy, here's a joke for you. " + joke, 8000)

				print("We have told you a joke!")

				last_method_to_increase_happiness = "joke"
				just_told_a_joke = True

			if method_to_make_you_happier_count == 1:
				## CROP PICTURE TO YOUR FACE ONLY AND TWEET IT

				height = frame.shape[0]
				#print(height)
				width = frame.shape[1]
				#print(width)
				x1 = parsed[0]["faceRectangle"]["left"] - 70
				x2 = x1 + 70 + parsed[0]["faceRectangle"]["width"] + 70
				y1 = parsed[0]["faceRectangle"]["top"] - 150
				y2 = y1 + 150 + parsed[0]["faceRectangle"]["height"] + 70
				x1 = x1 if x1 > 0 else 0
				y1 = y1 if y1 > 0 else 0
				x2 = x2 if x2 < width else width - 1
				y2 = y2 if y2 < height else height - 1
				#print(x1, x2, y1, y2)

				cropped_frame = frame[y1:y2, x1:x2]
				cropped_frame_image = Image.fromarray(cropped_frame)
				cropped_frame_image.save('crop.png')
				cropped_frame = cv2.imread('crop.png')
				cropped_frame = cv2.cvtColor(cropped_frame,cv2.COLOR_BGR2RGB)
				cv2.putText(cropped_frame,("Happiness Level: " + str("%.1f"%(happiness_level*100))+"%"),(0,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),thickness=2)
				cv2.imwrite('crop.png',cropped_frame)

				#tweet.tweet("sad", cropped_frame)
				#cv2.imshow("cropped", cropped_frame)
				#cv2.waitKey(0)

				tweet.tweet("I'm feeling " + str(float(parsed[0]['scores']['happiness'])*100) + "% happy  #OxfordHack", 'crop.png')

				print("We have tweeted to get you help!")

				last_method_to_increase_happiness = "tweet"

			if method_to_make_you_happier_count == 2:
				## PLAY CAT VIDEO

				openurl.play_cat_video()

				print("We have played a funny cat video!")

				last_method_to_increase_happiness = "video"

			method_to_make_you_happier_count = (method_to_make_you_happier_count + 1) % 3

		else:

			print("You're happy!")








#	k = cv2.waitKey(1)
#	count = count + 1
#	time.sleep(delay)

## When everything done, release the capture
#cam.release()
#cv2.destroyAllWindows()
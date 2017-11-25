import numpy
import cv2 

import cognitive_face as CF
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json

import time


##################################
# Configuration
##################################

# Path to folder with images
folder = 'file'
# Time delay between frames in seconds
delay = 2.5


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


	k = cv2.waitKey(1)
	count = count + 1
	time.sleep(delay)



# pathToFileInDisk = r'D:\tmp\3.jpg'
# with open( pathToFileInDisk, 'rb' ) as f:
#     data = f.read()
    
# # Computer Vision parameters
# params = { 'visualFeatures' : 'Color,Categories'} 

# headers = dict()
# headers['Ocp-Apim-Subscription-Key'] = _key
# headers['Content-Type'] = 'application/octet-stream'

# json = None

# result = processRequest( json, data, headers, params )





# cv2.imshow("Test Picture", frame) # displays captured image


# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()
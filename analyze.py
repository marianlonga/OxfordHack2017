import cognitive_face as CF
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json

KEY = 'bb72da8595ab4d56a05a1d666f7933f6'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
<<<<<<< HEAD

=======
result = CF.face.detect(img_url)
print (result)
>>>>>>> fa71533bc3e38b2956293b6f8c524e1468268845


uri_base = 'https://westcentralus.api.cognitive.microsoft.com'

# Request headers.
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': KEY,
}

# Request parameters.
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

# Body. The URL of a JPEG image to analyze.
<<<<<<< HEAD
body = {'url': img_url}
=======
body = {'url': 'https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg'}
>>>>>>> fa71533bc3e38b2956293b6f8c524e1468268845

try:
    # Execute the REST API call and get the response.
    response = requests.request('POST', uri_base + '/face/v1.0/detect', json=body, data=None, headers=headers, params=params)

    print ('Response:')
    parsed = json.loads(response.text)
    print (json.dumps(parsed, sort_keys=True, indent=2))

except Exception as e:
    print('Error:')
    print(e)
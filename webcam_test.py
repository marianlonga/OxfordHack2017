import numpy
import cv2 

cam = cv2.VideoCapture(0)


# Pause 


# while(True):
    # Capture frame-by-frame
ret, frame = cam.read()

cv2.imwrite("file/frame%d.jpg" % 1, frame)

cv2.imshow("Test Picture", frame) # displays captured image


# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()
import cv2

vidcap = cv2.VideoCapture('img_4359.mp4')
success,image = vidcap.read()
count = 0
success = True
while success:
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    cv2.imwrite("file/frame%d.jpg" % count, image)     # save frame as JPEG file
    count += 1

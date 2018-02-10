#importing modules
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

#capturing video through webcam
#cap=cv2.VideoCapture(0)
#creates a picamera object
camera = PiCamera()

camera.resolution = (640, 480)
#identifies frame rate
camera.framerate = 32
rawCapture = PiRGBArray(camera)

#defining the range of red color
red_lower=np.array([136,87,111],np.uint8)
red_upper=np.array([180,255,255],np.uint8)

#defining the Range of Blue color
blue_lower=np.array([100,10,10],np.uint8)
blue_upper=np.array([250,100,100],np.uint8)

#defining the Range of yellow color
yellow_lower=np.array([22,60,200],np.uint8)
yellow_upper=np.array([60,255,255],np.uint8)

# Currently unused.
# out = cv2.VideoWriter('output.avi', -1, 20, (640, 480))

print 'Red, Green, Blue'
for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):

	img = frame.array
	#converting frame(img i.e BGR) to HSV (hue-saturation-value)
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	#finding the range of red,blue and yellow color in the image
	red=cv2.inRange(hsv, red_lower, red_upper)
	blue=cv2.inRange(hsv,blue_lower,blue_upper)
	yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)

	#Morphological transformation, Dilation
	kernal = np.ones((5 ,5), "uint8")


	red=cv2.dilate(red, kernal)
	res=cv2.bitwise_and(img, img, mask = red)

	blue=cv2.dilate(blue,kernal)
	res1=cv2.bitwise_and(img, img, mask = blue)

	yellow=cv2.dilate(yellow,kernal)
	res2=cv2.bitwise_and(img, img, mask = yellow)

	Red = False
	Blue = False
	Green = False

	#Tracking the Blue Color
	(contours,hierarchy)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x,y,w,h = cv2.boundingRect(contour)
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			cv2.putText(img,"Blue color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,0,0))
			Blue = True

	#Tracking the pink Color
	(contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):

			x,y,w,h = cv2.boundingRect(contour)
			# The selected color was somewhat random, but it's actually close enough anyways.
			cv2.rectangle(img,(x,y),(x+w,y+h),(122,0,255),2)
			cv2.putText(img,"P",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(122,0,255))
			Red = True

	#Tracking the yellow Color
	(contours,hierarchy)=cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x,y,w,h = cv2.boundingRect(contour)
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
			cv2.putText(img,"Y",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1.0,(0,255,0))
			Green = True
	print '{}, {}, {}'.format(Red, Blue, Green)


	cv2.imshow("Color Tracking",img)
	# Force a wait time of 1 ms to take input.
	if cv2.waitKey(1) & 0xFF == ord('q'):
		camera.close()
		cv2.destroyAllWindows()
		break
	# Effectively dump whatever we had before.
	rawCapture.truncate(0)

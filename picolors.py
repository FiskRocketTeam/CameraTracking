import cv2
import numpy as np
import time

capture = cv2.VideoCapture(0)

# fourcc = cv2.cv.CV_FOURCC(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20, (640, 480))


# lower_red = np.uint8([136, 87, 111])
# upper_red = np.uint8([180, 255, 255])

# Between 160 and 200 as absolute lows and highs works.
lower_red = np.uint8([160, 50, 50])
upper_red = np.uint8([180, 255, 255])

# These colors work flawlessly, at least on the laptop webcam.
lower_blue = np.uint8([100, 50, 50])
upper_blue = np.uint8([120, 255, 255])

# Yellow range seems to work just fine.
lower_yellow = np.uint8([15, 100, 100])
upper_yellow = np.uint8([35, 255, 255])

runtime = 10
starttime = time.time()
while abs(starttime - time.time()) < runtime:
    ret, img = capture.read()

    # By putting this up here, the playback appears at normal speed.
    key = cv2.waitKey(1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask    = cv2.inRange(hsv, lower_red,    upper_red)
    blue_mask   = cv2.inRange(hsv, lower_blue,   upper_blue)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    total_mask  = cv2.bitwise_or(red_mask,   blue_mask)
    total_mask  = cv2.bitwise_or(total_mask, yellow_mask)
    blacked_img = cv2.bitwise_and(hsv, hsv,  mask=total_mask)

    # cv2.imshow('joined mask', blacked_img)
    out.write(blacked_img)


cv2.destroyAllWindows()
capture.release()
out.release()

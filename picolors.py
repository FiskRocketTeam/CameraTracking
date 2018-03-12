import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import time

camera = PiCamera()
camera.resolution = (640, 480)

# Set up a stream to dump camera info into.
rawCapture = PiRGBArray(camera)

# For use on the Raspberry Pi.
fourcc = cv2.cv.CV_FOURCC(*'XVID')

# For use on other systems.
# fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Output stream for video.
out = cv2.VideoWriter('output.avi', fourcc, 20, (640, 480))

# Establish hsv color ranges for our targets.

# Between 160 and 200 as absolute lows and highs works.
lower_red = np.uint8([160, 50, 50])
upper_red = np.uint8([180, 255, 255])

# These colors work flawlessly, at least on the laptop webcam.
lower_blue = np.uint8([100, 50, 50])
upper_blue = np.uint8([120, 255, 255])

# Yellow range seems to work just fine.
lower_yellow = np.uint8([15, 100, 100])
upper_yellow = np.uint8([35, 255, 255])

# Set the runtime of the program to ten seconds.
runtime = 10
starttime = time.time()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
# Replace the while loop with a broken for loop.
    if abs(starttime - time.time()) > runtime:
        break
# while abs(starttime - time.time()) < runtime:
#     img = camera.capture(rawCapture, format = "bgr", use_video_port=True).array
    # By putting this up here, the playback appears at normal speed as the
    # framerate is forced to drop a little bit.
    key = cv2.waitKey(1)

    # Convert the color to be something a little more useful in finding ranges.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Find masks where red, blue, and yellow appear.
    red_mask    = cv2.inRange(hsv, lower_red,    upper_red)
    blue_mask   = cv2.inRange(hsv, lower_blue,   upper_blue)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Use the masks generated to find all locations where color appears to
    # exist in frame, and use that to black out everything else.
    total_mask  = cv2.bitwise_or(red_mask,   blue_mask)
    total_mask  = cv2.bitwise_or(total_mask, yellow_mask)
    blacked_img = cv2.bitwise_and(hsv, hsv,  mask=total_mask)

    cv2.imshow('joined mask', blacked_img)
    out.write(blacked_img)

    # Remove all data from the previous frame.
    rawCapture.truncate(0)


# Close everything that we have open.
cv2.destroyAllWindows()
camera.close()
out.release()

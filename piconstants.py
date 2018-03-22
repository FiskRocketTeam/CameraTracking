import cv2
import numpy as np

HEIGHT = 480
WIDTH  = 640

FONT = cv2.FONT_HERSHEY_SIMPLEX
PINK_FONT   = np.uint8([255, 0, 0])
BLUE_FONT   = np.uint8([0, 0, 255])
YELLOW_FONT = np.uint8([0, 255, 0])
PINK_POS    = (460,  20)
BLUE_POS    = (460, 120)
YELLOW_POS  = (460, 220)
FONT_SCALE  = 1
LINE_TYPE   = 2

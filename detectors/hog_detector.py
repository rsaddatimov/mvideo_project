from imutils.object_detection import non_max_suppression
import cv2
import numpy as np

class HOGDetector:
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect(self, frame):
        rects, weights = self.hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

        rects = np.array([[x, y, x + w, y + h] for x, y, w, h in rects])
        rects = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        return [[x, y, xx - x, yy - y] for x, y, xx, yy in rects]

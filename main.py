import logging
import argparse
import numpy as np
import cv2
from imutils.object_detection import non_max_suppression
import imutils

#command line arguments parsing

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('-i', '--input', help='Path to CCTV cam ip file')
arg_parser.add_argument('-l', '--log', help='Path to log file')

args = arg_parser.parse_args()

if not args.input:
    raise Exception('No input file')

if args.log:
    logging.basicConfig(filename=args.log, level=logging.INFO, format='[%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

logging.info('Preparing...')
stream = cv2.VideoCapture(args.input)

cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Frame', 850, 500)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
frame_id = 1

logging.info('Starting video stream...')
while True:
    ret, frame = stream.read()

    frame = imutils.resize(frame, 800, 600)

    rects, weights = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

    rects = np.array([[x, y, x + w, y + h] for x, y, w, h in rects])
    rects = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    logging.info('%d-th frame: Detected %d objects...' % (frame_id, len(rects)))

    for x, y, xx, yy in rects:
        cv2.rectangle(frame, (x, y), (xx, yy), (0, 0, 255), 2)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_id += 1

logging.info('Ending stream...')

stream.release()
cv2.destroyAllWindows()

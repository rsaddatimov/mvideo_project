import logging
import argparse
import numpy as np
import cv2
import imutils
from detectors.hog_detector import HOGDetector

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

input_file = open(args.input, 'r')
file_names = [line.strip() for line in input_file]
input_file.close()

stream = cv2.VideoCapture(file_names[0])

cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Frame', 850, 500)

hog = HOGDetector()
frame_id = 1

logging.info('Starting video stream...')
while True:
    ret, frame = stream.read()

    frame = imutils.resize(frame, 800, 600)

    rects = hog.detect(frame)

    logging.info('%d-th frame: Detected %d objects...' % (frame_id, len(rects)))

    for x, y, h, w in rects:
        cv2.rectangle(frame, (x, y), (x + h, y + w), (0, 0, 255), 2)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_id += 1

logging.info('Ending stream...')

stream.release()
cv2.destroyAllWindows()

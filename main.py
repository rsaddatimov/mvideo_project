import argparse
import cv2
import numpy as np

#command line arguments parsing

argParser = argparse.ArgumentParser()

argParser.add_argument('--channel', required=True, type=int, help='The CCTV channel to listen')
argParser.add_argument('--debug-mode', action='store_true', help='Enables debug mode in which we draw and write frames')
argParser.add_argument('--fps-multiplier', type=int, default=1, help='The FPS multiplier')
argParser.add_argument('--gpu-enabled', action='store_true', help='Flag to enable CUDA GPU Backend')
argParser.add_argument('--min-confidence', type=float, default=0.5, help='The minimal acceptable confidence of detection')
argParser.add_argument('--model-path', required=True, type=str, help='Path to the model')
argParser.add_argument('--nms-threshold', type=float, default=0.3, help='The threshold of non-maximum suppression')
argParser.add_argument('--polygon-path', required=True, type=str, help='Path to the polygon')
argParser.add_argument('--start-time', required=True, type=str, help='Timestamp from which we listen channel')

argv = argParser.parse_args()


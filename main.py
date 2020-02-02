import argparse
import cv2
import numpy as np

from datetime import *
from detectors import YoloDetector
from geometry import Polygon
from graphics import drawDebug
from ioapi.multicam import RemoteMultiCapture
from os import getenv
from urllib.parse import quote_plus

# Обрабатываем аргументы командной строки
argParser = argparse.ArgumentParser()

argParser.add_argument('--channel', required=True, type=int, help='The CCTV channel to listen')
argParser.add_argument('--debug-mode', action='store_true', help='Enables debug mode in which we draw and write frames')
argParser.add_argument('--fps-multiplier', type=int, default=1, help='The FPS multiplier')
argParser.add_argument('--gpu-enabled', action='store_true', help='Flag to enable CUDA GPU Backend')
argParser.add_argument('--min-confidence', type=float, default=0.5, help='The minimal acceptable confidence of detection')
argParser.add_argument('--model-path', required=True, type=str, help='Path to the model')
argParser.add_argument('--nms-threshold', type=float, default=0.3, help='The threshold of non-maximum suppression')
argParser.add_argument('--polygon-path', required=True, type=str, help='Path to the polygon')
argParser.add_argument('--start-time', required=True, type=str, help='Timestamp from which we listen channel, which corresponds to the format d.m.Y H:M:S')

argv = argParser.parse_args()

CCTV_TOKEN = getenv('CCTV_TOKEN', 'secret-key')
CCTV_IP = getenv('CCTV_IP', 'localhost')

# Инициализируем видеопоток
remoteCapture = RemoteMultiCapture('ws://' + CCTV_IP + '/api?token=' + quote_plus(CCTV_TOKEN))
remoteCapture.channels = [argv.channel]
remoteCapture.fpsx = argv.fps_multiplier
remoteCapture.pos = datetime.strptime(argv.start_time, '%d.%m.%Y %H:%M:%S')

# Инициализируем детектор
detector = YoloDetector(
    argv.model_path,
    argv.min_confidence,
    argv.nms_threshold,
    argv.gpu_enabled
)

ouputWriter = None
if argv.debug_mode:
    outputWriter = cv2.VideoWriter(
        'output.avi',
        cv2.VideoWriter_fourcc('M','J','P','G'),
        10,
        (1280, 720)
    )

# Инициализируем полигон
polygon = Polygon()
polygon.load(argv.polygon_path)

# Начинаем процесс
while True:
    grabSuccess, frameData = remoteCapture.read()

    if not grabSuccess:
        break

    frameData = frameData[0]
    frame = frameData.image

    detections, confidences = detector.detect(frame)

    if argv.debug:
        outputWriter.write(drawDebug(
            frame,
            detections,
            polygon
        ))




if argv.debug_mode:
    outputWriter.release()



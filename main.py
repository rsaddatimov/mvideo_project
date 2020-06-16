import argparse
import numpy as np

from ioapi.multicam import RemoteMultiCapture
from ioapi.utils import FPSMeter, env
from urllib.parse import quote_plus
from datetime import *
from graphics import drawDebug
from os import getenv
import logging
import cv2
from detectors import YoloDetector
from notify import notify_manager

# Обрабатываем аргументы командной строки
argParser = argparse.ArgumentParser()

argParser.add_argument('--channel', required=True, type=int, help='The CCTV channel to listen')
argParser.add_argument('--debug-mode', action='store_true', help='Enables debug mode in which we draw and write frames')
argParser.add_argument('--fps-multiplier', type=int, default=1, help='The FPS multiplier')
argParser.add_argument('--gpu-enabled', action='store_true', help='Flag to enable CUDA GPU Backend')
argParser.add_argument('--min-confidence', type=float, default=0.5, help='The minimal acceptable confidence of detection')
argParser.add_argument('--model-path', required=True, type=str, help='Path to the model')
argParser.add_argument('--nms-threshold', type=float, default=0.3, help='The threshold of non-maximum suppression')
argParser.add_argument('--start-time', required=True, type=str, help='Timestamp from which we listen channel, which corresponds to the format d.m.Y H:M:S')
argParser.add_argument('--queue-threshold', required=True, type=int, help='Number of people in line that is considered to be a queue')
argParser.add_argument('--smtp-server', required=True, type=str, help='SMTP server')
argParser.add_argument('--manager-email', required=True, type=str, help="Manager's email address where notification will be sent")
argParser.add_argument('--sender-email', required=True, type=str, help="Sender's email address from which notification will be sent")
argParser.add_argument('--sender-password', required=True, type=str, help="Sender's email password")
argParser.add_argument('--wait-cooldown', required=True, type=int, help='Cooldown between notifications (in seconds)')

argv = argParser.parse_args()

# TOKEN и IP должны быть в переменных окружения
CCTV_TOKEN = getenv('CCTV_TOKEN', 'secret-key')
CCTV_IP = getenv('CCTV_IP', 'localhost')

# Инициализируем видеопоток
remoteCapture = RemoteMultiCapture('ws://' + CCTV_IP + '/api?token=' + quote_plus(CCTV_TOKEN))
remoteCapture.channels = [argv.channel]
remoteCapture.fpsx = argv.fps_multiplier
remoteCapture.pos = datetime.strptime(argv.start_time, '%d.%m.%Y %H:%M:%S')


# Последние n секунд
avg_sec = 10

# Запись видео для дебага
outputWriter = None
if argv.debug_mode:
    outputWriter = cv2.VideoWriter(
        'output.avi',
        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
        30,
        (1280, 720)
    )

# Инициализируем видеопоток
remoteCapture = RemoteMultiCapture('ws://' + CCTV_IP + '/api?token=' + quote_plus(CCTV_TOKEN))
remoteCapture.channels = [argv.channel]
remoteCapture.fpsx = argv.fps_multiplier
remoteCapture.pos = datetime.strptime(argv.start_time, '%d.%m.%Y %H:%M:%S')
# fps = FPSMeter(autodump=1)
fps = 24

# Инициализируем детектор
detector = YoloDetector(
    argv.model_path,
    argv.min_confidence,
    argv.nms_threshold,
    argv.gpu_enabled
)

# Счетчики
ppl_this_sec = 0
frames_this_sec = 0
prev_results = [0] * avg_sec
seconds_passed = 0
cooldown = 0

while True:
    # пробуем считать кадр
    try:
        ret, frames = remoteCapture.read()
    except Exception:
        pass
    if not ret: break
    for frame in frames:
        frames_this_sec += 1
        if frames_this_sec == fps:
            seconds_passed += 1
            if cooldown > 0:
                cooldown += 1
            if cooldown == argv.wait_cooldown:
                cooldown = 0
            if seconds_passed == avg_sec:
                seconds_passed = 0
            
            prev_results[seconds_passed] = ppl_this_sec
            ppl_this_sec = 0
            frames_this_sec = 0
            
        ''' 
        Если в последние несколько секунд было обнаружено более q людей,
        считаем, что образовалась очередь, и уведомляем менеджера, в случае,
        когда с прошлого уведомления прошло wait_cooldown секунд.
        '''
        if not cooldown and sum(prev_results) / avg_sec >= argv.queue_threshold:
            notify_manager(argv.smtp_server, 
                           argv.manager_email, 
                           argv.sender_email, 
                           argv.sender_password, 
                           argv.channel
                           )
            cooldown += 1
                
        # Определяем количество людей в кадре
        detection_output = detector.detect(frame)
        predicted_number = len(detection_output[0])
        ppl_this_sec += predicted_number / fps
            
        
    # процесс можно остановить по нажатию клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'): break

    
if argv.debug_mode:
    outputWriter.release()
    

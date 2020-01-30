import cv2
import numpy as np
from os.path import exists

"""
Класс для детектирования с помощью ssd модели
Метод ещё не проверен на точность
"""
class SSDDetector:


    def __init__(self, protoPath, modelPath, confidence=0.0):
        if modelPath is None or protoPath is None:
            raise Exception('Path to the model cant be None!')
        if not exists(protoPath) or not exists(modelPath):
            raise Exception('Model was not found at %s ans %s' % (modelPath, protoPath))

        self.net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
        self.confidence = confidence

    def reload_model(self, protoPath, modelPath):
        logging.info('Reloading DNN model...')
        try:
            self.net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
            logging.info('DNN model was reloaded succesfully...')
        except Exception as e:
            logging.error(e)

    def detect(self, frame):
        (H, W) = frame.shape[:2]
        mulMatrix = np.array([W, H, W, H])

        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        self.net.setInput(blob)
        detections = self.net.forward()

        rects = []
        for i in range(detections.shape[2]):
            probability = detections[0, 0, i, 2]
            detectedId = int(detections[0, 0, i, 1])

            if probability <= self.confidence or detectedId != 15:
                continue

            rect = detections[0, 0, i, 3 : 7] * mulMatrix
            (startX, startY, endX, endY) = rect.astype("int")
            rects.append([startX, startY, endX - startX, endY - startY])

        return rects

import cv2
import numpy as np
from os.path import join as pj
from os.path import exists


"""
 Класс для детектирования людей на кадре с
 использованием YOLO
"""
class YoloDetector:

    def __init__(self, modelPath):
        if not exists(modelPath):
            raise Exception('Model was not found at %s' % modelPath)
        self.net = cv2.dnn.readNetFromDarknet(pj(modelPath, 'yolo3.cfg'), pj(modelPath, 'yolo3.weights'))

    def detect(self, inputFrame):
        blob = cv2.dnn.blobFromImage(inputFrame, 1 / 255.0, (416, 416), swapRB=True, crop=False)

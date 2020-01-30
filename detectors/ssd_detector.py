import cv2
import numpy as np
from os.path import exists

"""
Класс для детектирования с помощью ssd модели
Метод ещё не проверен на точность
С GPU работает, но может и не работать
"""
class SSDDetector:

    """
    Конструктор класса
    @in protoPath - путь к прото файлику модели
    @in modelPath - путь к самой модели
    @in confidence - минимально допустимая вероятность обнаружения
    """
    def __init__(self, protoPath, modelPath, confidence):
        if modelPath is None or protoPath is None:
            raise Exception('Path to the model cant be None!')
        if not exists(protoPath) or not exists(modelPath):
            raise Exception('Model was not found at %s ans %s' % (modelPath, protoPath))

        self.net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
        self.confidence = confidence

        self.backScaleArray = None

    """
    Метод для загрузки другой модели
    @in protoPath - путь к прото файлику модели
    @in modelPath - путь к самой модели
    """
    def reload_model(self, protoPath, modelPath):
        if modelPath is None or protoPath is None:
            raise Exception('Path to the model cant be None!')
        if not exists(protoPath) or not exists(modelPath):
            raise Exception('Model was not found at %s ans %s' % (modelPath, protoPath))

        self.net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

    """
    Метод, который по кадру дает детекты на ней в виде массива прямоугольников
    @in inputFrame - подаваемый на обработку кадр
    @return - лист из прямоугольников
    """
    def detect(self, frame):
        if self.backScaleArray is None:
            (H, W) = frame.shape[:2]
            self.backScaleArray = np.array([W, H, W, H])

        blob = cv2.dnn.blobFromImage(
            frame,
            0.007843,
            (300, 300),
            127.5
        )

        self.net.setInput(blob)
        detections = self.net.forward()

        rects = []
        for i in range(detections.shape[2]):
            probability = detections[0, 0, i, 2]
            detectedId = int(detections[0, 0, i, 1])

            if probability <= self.confidence or detectedId != 15:
                continue

            rect = detections[0, 0, i, 3 : 7] * self.backScaleArray
            (startX, startY, endX, endY) = rect.astype("int")
            rects.append([startX, startY, endX - startX, endY - startY])

        return rects

import cv2
import numpy as np
from os.path import join as pj
from os.path import exists


"""
 Класс для детектирования людей на кадре с
 использованием YOLO
"""
class YoloDetector:

    """
    Кокструктор класса. Инициализирует всё необходимое
    @in mdelPath - путь к модели
    @in confidence - минимально допустимая вероятность обнаружения
    @in threshold
    """
    def __init__(self, modelPath, confidence, threshold):
        if not exists(pj(modelPath, 'yolo3.cfg')) or not exists(pj(modelPath, 'yolo3.weights')):
            raise Exception('Model was not found at %s' % modelPath)

        self.net = cv2.dnn.readNetFromDarknet(
            pj(modelPath, 'yolo3.cfg'),
            pj(modelPath, 'yolo3.weights')
        )

        self.layersNames = self.net.getLayerNames()
        self.layersNames = [self.layersNames[id[0] - 1] for id in self.net.getUnconnectedOutLayers()]

        self.acceptableConfidence = confidence
        self.threshold = threshold

        self.backScaleArray = None

    """
    Метод, который по кадру дает детекты на ней в виде массива прямоугольников
    @in inputFrame - подаваемый на обработку кадр
    @return - лист из прямоугольников
    """
    def detect(self, inputFrame):
        if self.backScaleArray:
            (H, W) = inputFrame.shape[:2]
            self.backScaleArray = np.array([W, H, W, H])

        # Скармливаем нейронке кадр
        blob = cv2.dnn.blobFromImage(
            inputFrame,
            1 / 255.0,
            (416, 416),
            swapRB=True,
            crop=False
        )
        self.net.setInput(blob)
        outputLayers = self.net.forward(self.layersNames)

        resultingRectangles = []
        resultingConfidences = []

        # Итерируемся по обнаружениям
        for layer in outputLayers:
            for detection in layer:
                probabilities = detection[5:]
                classId = np.argmax(probabilities)
                confidence = probabilities[classId]

                # Проверяем подходит ли нам детект
                # В данном случае classId должен быть равен 0, так как 0 соответствует человеку
                if classId or confidence <= self.acceptableConfidence:
                    continue

                # Строим прямоугольник и добавляем его к обнаружениям
                rect = detection[0:4] * self.backScaleArray
                (centerX, centerY, width, height) = rect.astype("int")
                cornerX = int(centerX - (width / 2))
                cornerY = int(centerY - (height / 2))

                resultingRectangles.append([cornerX, cornerY, int(width), int(height)])
                resultingConfidences.append(confidence)

                # Не забываем применить non-maximum suppression чтобы
                # избавиться от неоправданных пересечений прямоугоьлников
                resultingRectangles = cv2.dnn.NMSBoxes(
                    resultingRectangles,
                    resultingConfidences,
                    self.acceptableConfidence,
                    self.threshold
                )

                return resultingRectangles, resultingConfidences

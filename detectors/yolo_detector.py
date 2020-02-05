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
    @in modelPath - путь к модели
    @in confidence - минимально допустимая вероятность обнаружения
    @in threshold
    """
    def __init__(self, modelPath, confidence=0.5, threshold=0.3, gpuEnabled=False):
        if not exists(pj(modelPath, 'yolov3.cfg')) or not exists(pj(modelPath, 'yolov3.weights')):
            raise Exception('Model was not found at %s' % modelPath)

        self.net = cv2.dnn.readNetFromDarknet(
            pj(modelPath, 'yolov3.cfg'),
            pj(modelPath, 'yolov3.weights')
        )

        if gpuEnabled:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        self.layersNames = self.net.getUnconnectedOutLayersNames()

        self.acceptableConfidence = confidence
        self.threshold = threshold

    """
    Метод, который по кадру дает детекты на ней в виде массива прямоугольников
    @in inputFrame - подаваемый на обработку кадр
    @return - лист из прямоугольников
    """
    def detect(self, inputFrame):
        (H, W) = inputFrame.shape[:2]

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
                rect = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = rect.astype("int")
                cornerX = int(centerX - (width / 2))
                cornerY = int(centerY - (height / 2))

                resultingRectangles.append([int(cornerX), int(cornerY), int(width), int(height)])
                resultingConfidences.append(float(confidence))

        if len(resultingRectangles) == 0:
            return [], []

        # Не забываем применить non-maximum suppression чтобы
        # избавиться от неоправданных пересечений прямоугоьлников
        resultingRectangles = cv2.dnn.NMSBoxes(
            resultingRectangles,
            resultingConfidences,
            self.acceptableConfidence,
            self.threshold
        )

        return [resultingRectangles[id[0]] for id in acceptableIndices], resultingConfidences

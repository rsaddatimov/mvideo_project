from imutils.object_detection import non_max_suppression
import cv2
import numpy as np


"""
Класс для детектирования с помощью метода Histogram of gradients
ВНИМАНИЕ! ОЧЕНЬ ПЛОХОЙ ПО ТОЧНОСТИ МЕТОД
"""
class HOGDetector:

    """
    Конструктор класса
    """
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    """
    Метод детектирующий людей
    @in frame - поступающий кадр
    @return - лист прямоугольников
    """
    def detect(self, frame):
        # Извлекаем обнаружения
        rects, weights = self.hog.detectMultiScale(
            frame,
            winStride=(4, 4),
            padding=(8, 8),
            scale=1.05
        )

        rects = np.array([[x, y, x + w, y + h] for x, y, w, h in rects])

        # Не забываем применить non-maximum suppression чтобы
        # избавиться от неоправданных пересечений прямоугоьлников
        rects = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        return [[x, y, rx - x, ry - y] for x, y, rx, ry in rects]

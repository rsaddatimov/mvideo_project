from geometry import Point
from typing import List


"""
Класс для работы с многоугольникам в двумерном пространстве
"""
class Polygon:

    """
    Конструктор класса
    @in vertexList - список точек
    """
    def __init__(self, vertexList: List[Point]):
        self.vertices = vertexList
        self.vertexCount = len(self.vertices)

    """
    Метод проверяющий по данной точке, лежит ли она внутри данного
    многоугольника. Работает ассимптотически за O(vertexCount)
    @in pt - проверяемая точка
    @return bool - True если лежит, иначе False
    """
    def pointInside(self, pt: Point):
        cnt, key = 0, False

        for i in range(1, self.vertexCount + 1):
            if (pt.x < self.vertices[i - 1].x or pt.x < self.vertices[i % self.vertexCount].x) \
                and pt.y > min(self.vertices[i - 1].y, self.vertices[i % self.vertexCount].y) \
                and pt.y < max(self.vertices[i - 1].y, self.vertices[i % self.vertexCount].y):
                cnt += 1

        for i in range(self.vertexCount):
            tmp = (self.vertices[(i + 1) % self.vertexCount].x - self.vertices[i].x) \
                * (pt.y - self.vertices[i].y) - (pt.x - self.vertices[i].x) \
                * (self.vertices[(i + 1) % self.vertexCount].y - self.vertices[i].y)

            if tmp == 0 and pt.x >= min(self.vertices[(i + 1) % self.vertexCount].x, self.vertices[i].x) \
                and pt.x <= max(self.vertices[(i + 1) % self.vertexCount].x, self.vertices[i].x):
                key = True
                break

        return ((cnt % 2 == 1) or key)

    """
    Метод проверяющий по данной точке, лежит ли она внутри данного
    многоугольника. Работает ассимптотически за O(log(vertexCount))
    @in pt - проверяемая точка
    @return bool - True если лежит, иначе False
    """
    def pointInsideFast(self, pt: Point):
        # TODO @rsaddatimov
        raise NotImplementedError

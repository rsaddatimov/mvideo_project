from geometry import Point
from os.path import exists
from types import *
from typing import List


"""
Класс для работы с многоугольникам в двумерном пространстве
@property vertices - список вершин (точки типа Point)
@property vertexCount - количество вершин
"""
class Polygon:

    """
    Конструктор класса
    @in vertexList - список точек
    """
    def __init__(self):
        self.vertices = None
        self.vertexCount = None

    """
    Метод для подгрузки вершин полигона. Перегрузжен
    @in arg: str - подгружаем полигон из файлика
    @in arg: List[Point] - подгружаем из уже существующего списка
    """
    def load(self, arg):
        if arg is None:
            raise Exception("arg must not be None type")
        elif isinstance(arg, str):
            if not exists(arg):
                raise Exception("Polygon was not found at %s" % arg)

            file = open(arg, mode='r')

            try:
                self.vertexCount = int(file.readline())
                self.vertices = []
                for i in range(self.vertexCount):
                    x, y = map(int, file.readline().split())
                    self.vertices.append(Point(x, y))
            except Exception as e:
                print(e)

            file.close()
        elif isinstance(arg, list):
            for i in range(len(arg)):
                assert(isinstance(arg[i], Point))

            self.vertices = arg
            self.vertexCount = len(self.vertices)
        else:
            raise Exception("arg has unsupported initialization type for Polygon!")

    """
    Метод проверяющий по данной точке, лежит ли она внутри данного
    многоугольника. Работает ассимптотически за O(vertexCount)
    @in pt - проверяемая точка
    @return bool - True если лежит, иначе False
    """
    def pointInside(self, pt: Point):
        if self.vertexCount is None:
            raise Exception("Polygon is not initialized")
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

    """
    Метод вычисляющий расстояние от данной точки до полигона
    @in pt - точка
    @return float - расстояние
    """
    def distance(self, pt: Point) -> float:
        # TODO @rsaddatimov
        if self.pointInside(pt):
            return 0
        raise NotImplementedError

from math import sqrt


"""
Класс соответствующий точке в пространстве
"""
class Point:

    """
    Конструктор класса
    @in x - координата x точки
    @in y - координата y точки
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    """
    Расстояние от данной точки до другой
    @in other - точка Point
    @return double - расстояние от данной точки до другой
    """
    def distance(self, other: Point):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    """
    Расстояние между двумя точками. Статический метод
    @in first - точка Point
    @in secon - точка Point
    @return double - расстояние между ними
    """
    @staticmethod
    def distance(first, second):
        return sqrt((first.x - second.x) ** 2 + (first.y - second.y) ** 2)

from geometry import Point
from math import sqrt
from typing import List

class Polygon:

    def __init__(self, vertexList: List[Point]):
        self.vertices = vertexList
        self.vertexCount = len(self.vertices)

    def pointInside(self, pt: Point):
        
        return False

    def pointInsideFast(self, pt: Point):
        return False

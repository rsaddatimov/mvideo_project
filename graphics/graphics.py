import cv2

from geometry import Polygon

def drawDebug(
    frame,
    detections,
    polygon: Polygon
):
    # Рисуем полигон
    for i in range(polygon.vertexCount):
        x1 = polygon.vertices[i].x
        y1 = polygon.vertices[i].y
        x2 = polygon.vertices[(i + 1) % polygon.vertexCount].x
        y2 = polygon.vertices[(i + 1) % polygon.vertexCount].y
        cv2.line(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 0, 255),
            1
        )

        # Рисуем обнаружения
        for x, y, w, h in detections:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )


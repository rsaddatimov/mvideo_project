import cv2

from geometry import Point, Polygon

SHADE_DISTANCE = 150

#TODO @rsaddatimov
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
        rectCentre = Point(x + w / 2, y + h / 2)
        rectColor = (0, 255, 0) #green
        distanceToPoly = polygon.distance(rectCentre)

        if distanceToPoly < SHADE_DISTANCE:
            rectColor = Point.lerp(
                rectColor,
                (255, 0, 0),
                1 - distanceToPoly / SHADE_DISTANCE
            )

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            distanceToPoly,
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            rectColor,
            2
        )



from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.points_pos = []
        self.hull = []
        self.draw_convex = False


    def keyPressEvent(self, e):
        if e.modifiers() & Qt.ControlModifier and e.key() == Qt.Key_L:
            self.points = []
            self.points_pos = []
            self.hull = []
            self.draw_convex = False
            self.update()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.points.append(event.pos())
            self.points_pos.append((event.pos().x(), event.pos().y()))

        if event.button() == Qt.RightButton:
            print(self.andrew(self.points_pos))
            self.hull = self.andrew(self.points_pos)
            self.draw_convex = True

        self.update()


    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.points:
            return

        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 4.0))
        for i in range(len(self.points)):
            painter.drawPoint(QPoint(self.points[i]))
        
        painter.setPen(QPen(Qt.blue, 2.0))
        if self.draw_convex:
            for i in range(len(self.hull)):
                if ((self.hull[i][0], self.hull[i][1]) == self.rightmost_point):
                    painter.setPen(QPen(Qt.green, 2.0))
                painter.drawLine(QPoint(self.hull[i][0], self.hull[i][1]),
                                 QPoint(self.hull[(i + 1) % len(self.hull)][0], self.hull[(i + 1) % len(self.hull)][1]))

    def andrew(self, points):
        points = sorted(set(points))

        if len(points) <= 1:
            return points

        """
        Векторное произведение.
        > 0, если правый поворот
        < 0, если левый поворот
        = 0, ecли коллинеарные
        """
        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        # Строим нижнюю оболочку
        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        # Строим верхнюю оболочку
        self.rightmost_point = points[-1]
        print(self.rightmost_point)
        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)

        return lower[:-1] + upper[:-1]

if __name__ == '__main__':
    app = QApplication([])

    w = Widget()
    w.show()
    app.exec()
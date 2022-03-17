import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main Window 정보 설정
        self.setWindowTitle("손글씨 그리기")
        self.resize(800, 600)
        ##

        # Canvas
        canvas = Canvas()
        ##

        # layout
        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(canvas, 0, 0)
        grid.addWidget(QLabel('Text'), 0, 1)
        ##

        self.show()


class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.start = QPointF()
        self.end = QPointF()
        self.initUI()

    def __del__(self):
        img = QPixmap()
        img = self.grab(self.sceneRect().toRect())
        img.save('img.png')

    def initUI(self):
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0,0,-2,-2)
 
        self.scene.setSceneRect(rect)

    def mousePressEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.start = e.pos()
            self.end = e.pos()

    def mouseMoveEvent(self, e):
        self.end = e.pos()
        pen = QPen(Qt.black, 10)

        if e.buttons() & Qt.LeftButton:
            path = QPainterPath()
            path.moveTo(self.start)
            path.lineTo(self.end)
            self.scene.addPath(path,pen)

            self.start = e.pos()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

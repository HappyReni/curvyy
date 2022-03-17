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
        self.setWindowTitle("Curvyy")
        self.resize(800, 600)
        ##

        # Components
        canvas = Canvas()
        textbox = QTextEdit()
        red_color = QColor(255, 96, 92)
        orange_color = QColor(255, 189, 68)
        green_color = QColor(0, 202, 78)

        red = Signal(red_color)
        orange = Signal(orange_color)
        green = Signal(green_color)
        ##

        # layout
        hbox = QHBoxLayout()
        self.setLayout(hbox)

        signalbox = QHBoxLayout()
        signalbox.addWidget(red)
        signalbox.addWidget(orange)
        signalbox.addWidget(green)
        signalbox.addStretch()
        signalbox.setSpacing(10)

        rightvbox = QVBoxLayout()
        rightvbox.addWidget(QLabel('Text'))
        rightvbox.addWidget(textbox)
        leftvbox = QVBoxLayout()
        leftvbox.addLayout(signalbox)
        leftvbox.addWidget(canvas)

        hbox.addLayout(leftvbox)
        hbox.addLayout(rightvbox)
        ##

        self.show()

class Signal(QWidget):
    def __init__(self,color):
        super().__init__()

        # self.setSizePolicy(
        #     QSizePolicy.MinimumExpanding,
        #     QSizePolicy.MinimumExpanding
        # )

        self.color = color
    
    def sizeHint(self):
        return QSize(20,20)

    def setColor(self,color):
        self.color = color
        self.update()

    def paintEvent(self, e):
        # qp = QPainter()
        # qp.begin(self)
        # qp.setRenderHint(QPainter.Antialiasing)
        # qp.setPen(QPen(self.color, 10))
        # qp.drawRoundedRect(1, 1, 100, 100, 50, 50)
        # # self.scene.addRect(1, 1, 100, 100,QPen(self.color, 10))
        # qp.end()
        painter = QPainter(self)

        painter.setPen(QPen(self.color))
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.color)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        painter.drawRoundedRect(0, 0, 20, 20, 60, 60)
        # painter.fillRect(rect, brush)
        painter.end()




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

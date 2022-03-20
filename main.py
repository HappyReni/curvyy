from enum import Enum
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def delay(n):
    loop = QEventLoop()
    QTimer.singleShot(n, loop.quit) # msec
    loop.exec_()

class SEQ(Enum):
    IDLE = 1,
    WRITING = 2,
    DONE = 3,
    
    SAVE =4,

class Manager():
    def __init__(self):
        super().__init__()
        self.seq = SEQ.IDLE
        
    def setState(self,app,state):
        if state == SEQ.IDLE:
            app.red.on()
            app.orange.off()
            app.green.off()
        
        elif state == SEQ.WRITING:
            app.red.off()
            app.green.off()
            app.orange.on()

        elif state == SEQ.DONE:
            app.red.off()
            app.green.off()
            app.orange.blink()
        
        elif state == SEQ.SAVE:
            app.red.off()
            app.orange.off()
            app.green.on()
            self.clearCanvas(app.canvas)
    
    def clearCanvas(self, app):
        app.clearScene()

manager = Manager()

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
        self.canvas = Canvas()
        textbox = QTextEdit()

        self.red = Signal("red")
        self.orange = Signal("orange")
        self.green = Signal("green")
        ##
        manager.setState(self,SEQ.IDLE)
        # layout
        hbox = QHBoxLayout()
        self.setLayout(hbox)

        signalbox = QHBoxLayout()
        signalbox.addWidget(self.red)
        signalbox.addWidget(self.orange)
        signalbox.addWidget(self.green)
        signalbox.addStretch()
        signalbox.setSpacing(10)

        rightvbox = QVBoxLayout()
        rightvbox.addWidget(QLabel('Text'))
        rightvbox.addWidget(textbox)

        leftvbox = QVBoxLayout()
        leftvbox.addLayout(signalbox)
        leftvbox.addWidget(self.canvas)

        hbox.addLayout(leftvbox)
        hbox.addLayout(rightvbox)
        ##

        self.show()

class Signal(QWidget):
    def __init__(self,type):
        super().__init__()
        self.state = False

        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        
        self.initColor(type)

    def initColor(self,type):
        if type == "red":
            self.color_on = QColor(255, 96, 92)
            self.color_off = QColor(179, 67, 64)
        elif type == "orange":
            self.color_on = QColor(255, 189, 68)
            self.color_off = QColor(179, 132, 48)
        else:
            self.color_on = QColor(0, 202, 78)
            self.color_off = QColor(0, 101, 39)
        self.color = self.color_on

    def sizeHint(self):
        return QSize(20,20)

    def on(self):
        self.color = self.color_on
        self.effect.setOpacity(1)
        self.state = True
        self.update()

    def off(self):
        self.color = self.color_off
        self.effect.setOpacity(1)
        self.state = False
        self.update()
    
    def beginSave(self):
        pp = self.parent()
        manager.setState(pp, SEQ.SAVE)
    
    def blink(self):
        self.color_anim_s = QPropertyAnimation(self.effect, b'opacity')
        self.color_anim_s.setStartValue(1.0)
        self.color_anim_s.setEndValue(0.3)
        self.color_anim_s.setDuration(1000)
        self.color_anim_s.setLoopCount(2)

        self.color_anim_s.start()
        self.color_anim_s.finished.connect(self.off)
        self.color_anim_s.finished.connect(self.beginSave)

    def paintEvent(self, e):
        painter = QPainter(self)

        painter.setPen(QPen(self.color))
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(self.color)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.drawRoundedRect(0, 0, 20, 20, 60, 60)
        # painter.fillRect(rect, brush)
        painter.end()

class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.start = QPointF()
        self.end = QPointF()
        
        self.initUI()

    def initUI(self):
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

    def clearScene(self):
        pp = self.parent()
        img = QPixmap()
        img = self.grab(self.sceneRect().toRect())
        img.save('img.png')
        self.scene.clear()
        delay(1000)
        manager.setState(pp,SEQ.IDLE)
        
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
        pp = self.parent()

        if e.buttons() & Qt.LeftButton:
            manager.setState(pp,SEQ.WRITING)

            path = QPainterPath()
            path.moveTo(self.start)
            path.lineTo(self.end)
            self.scene.addPath(path,pen)

            self.start = e.pos()
    
    def mouseReleaseEvent(self,e):
        pp = self.parent()
        manager.setState(pp,SEQ.DONE)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

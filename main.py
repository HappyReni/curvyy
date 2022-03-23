import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import cv2
from PIL import Image
from tensorflow import keras
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from enum import Enum

config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.8
config.gpu_options.allow_growth = True
session = tf.compat.v1.InteractiveSession(config=config)

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
        self.str = ""
        self.model = self.loadModel()

    def setState(self,app,state):
        self.seq = state
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
            self.predict(app.textbox)

    def getState(self):
        return self.seq
    
    def clearCanvas(self, canvas):
        canvas.clearScene()

    def loadModel(self):
        model = keras.models.load_model("parameters.h5")
        model.compile(optimizer='sgd',loss='sparse_categorical_crossentropy',metrics='accuracy')
        return model

    def predict(self,textbox):
        mapp = pd.read_csv("data/emnist-balanced-mapping.txt", delimiter = ' ', \
                   index_col=0, header=None).squeeze("columns")
        img = cv2.imread("img.png")

        img = 255-img[:,:,0]
        img = np.fliplr(img)
        img = np.rot90(img)

        saveimg = Image.fromarray(img.reshape(28,28).astype(np.uint8))
        saveimg.save('example.png','png')

        img = img.reshape(1,28,28)

        result = self.model.predict(img)
        print(img)
        
        # plt.imshow(img.reshape(28,28),cmap='gray_r')
        # plt.show()
        pred_class = np.argmax(result)
        pred_letter = chr(mapp[pred_class])
        print(f"예측 문자 : {pred_letter}")

        self.str += pred_letter
        textbox.clear()
        textbox.setText(self.str)

manager = Manager()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main Window 정보 설정
        self.setWindowTitle("Curvyy")
        self.resize(600, 400)
        ##

        # Components
        self.canvas = Canvas()
        self.textbox = QTextEdit()

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
        rightvbox.addWidget(self.textbox)

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
        img = img.scaled(28,28,transformMode=Qt.SmoothTransformation)
        img.save('img.png')
        self.scene.clear()
        delay(500)
        manager.setState(pp,SEQ.IDLE)
        
    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0,0,-2,-2)
        self.scene.setSceneRect(rect)

    def mousePressEvent(self, e):
        pp = self.parent()

        if e.buttons() & Qt.LeftButton:
            self.start = e.pos()
            self.end = e.pos()
            manager.setState(pp,SEQ.WRITING)


    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & (manager.getState() == SEQ.WRITING):
            self.end = e.pos()
            pen = QPen(Qt.black, 30,Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin)
            path = QPainterPath()
            path.moveTo(self.start)
            path.lineTo(self.end)
            self.scene.addPath(path,pen)

            self.start = e.pos()
    
    def mouseReleaseEvent(self,e):
        if e.button() == Qt.LeftButton:
            pp = self.parent()
            manager.setState(pp,SEQ.DONE)
            super(Canvas, self).mouseReleaseEvent(e)

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()

    sys.exit(app.exec_())
# Ex 10-6. MNIST 손글씨 인식 프로그램.

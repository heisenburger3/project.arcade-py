import sys
import random
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPainter, QColor


class CircleSpawner(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.is_drew = False
        self.setWindowTitle('Супрематизм')
        self.pushButton.clicked.connect(self.draw)
        self.SCREEN_SIZE = [680, 480]
        self.size = random.randint(10, 100)
        self.color = (255, 255, 0)

    def draw(self):
        self.is_drew = True
        self.update()

    def paintEvent(self, event):
        if self.is_drew:
            qp = QPainter()
            qp.begin(self)
            qp.setPen(QColor(*self.color))
            qp.setBrush(QColor(*self.color))
            self.x, self.y = random.randint(100, self.SCREEN_SIZE[0] - 100), random.randint(100,
                                                                                            self.SCREEN_SIZE[1] - 100)
            qp.drawEllipse(self.x, self.y, self.size, self.size)
            qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CircleSpawner()
    ex.show()
    sys.exit(app.exec())

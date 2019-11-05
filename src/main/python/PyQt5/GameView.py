import sys

from PyQt5.QtWidgets import *

from python.PyQt5.GameMainWindow import GameMainWindow


class GameView(QMainWindow):

    def __init__(self):
        super(GameView, self).__init__()
        self.ui = GameMainWindow()
        self.ui.setup_ui(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    draughts = GameView()
    draughts.show()
    sys.exit(app.exec_())
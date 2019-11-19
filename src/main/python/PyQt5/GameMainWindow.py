# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GameMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!
import functools
import itertools

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from python.model.Board import Board
from python.model.BoardCell import BoardCell
from python.model.ComputerLogic import ComputerLogic
from python.model.Side import Side

board = Board(8, 8)

buttons = dict()

choose_cell_phase = True

in_progress = False

chosen_cell = None


class QGroupBoxClickable(QtWidgets.QGroupBox):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QGroupBox.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()


class GameMainWindow(object):
    def setup_ui(self, MainWindow):
        global in_progress
        global choose_cell_phase
        MainWindow.setObjectName("Draughts")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 181, 601))
        self.frame.setStyleSheet("QFrame {\n"
                                 "border-color:black;\n"
                                 "border-style:solid;\n"
                                 "border-width:5px;\n"
                                 "background-color:#FFFACD;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton {\n"
                                 "border-color:black;\n"
                                 "border-style:solid;\n"
                                 "set-fx-text-fill: black;\n"
                                 "background-color: #dcb35c;\n"
                                 "border-radius: 40px;\n"
                                 "border-width:3px;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:hover {\n"
                                 "background-color: #ECE7BC;\n"
                                 "}\n"
                                 "\n"
                                 "QLabel{\n"
                                 "border-color:black;\n"
                                 "border-style:solid;\n"
                                 "border-width:5 5 5 5;\n"
                                 "}")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 181, 111))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.restart = QtWidgets.QPushButton(self.frame)
        self.restart.setGeometry(QtCore.QRect(20, 160, 141, 81))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.restart.setFont(font)
        self.restart.setObjectName("restart")
        self.restart.pressed.connect(lambda : self.restart_pressed())
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(180, 0, 621, 601))
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        for vertical, horizontal in itertools.product(range(board.width), range(board.height)):
            board_cell = BoardCell(vertical, horizontal)
            groupBox = QGroupBoxClickable(self.widget)
            image_label = QtWidgets.QLabel(groupBox)
            image_label.setGeometry(QtCore.QRect(0, 0, 80, 80))
            if (vertical + horizontal) % 2 == 0:
                image_label.setStyleSheet("background-color:#fdeda8;")
            else:
                image_label.setStyleSheet("background-color:#ba7b55;")
            event = functools.partial(self.group_clicked, board_cell)
            groupBox.clicked.connect(event)
            buttons[board_cell] = groupBox
            self.gridLayout.addWidget(groupBox, horizontal, vertical, 1, 1)
            self.update_board(board_cell)
        in_progress = True
        self.update_status()
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslate_ui(MainWindow)
        self.label.update()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Draughts", "Draughts"))
        self.restart.setText(_translate("MainWindow", "Restart game"))

    def group_clicked(self, board_cell: BoardCell):
        global choose_cell_phase
        global chosen_cell
        group = buttons[board_cell]
        image_label = group.children()[0]
        if in_progress:
            if choose_cell_phase:
                if board.cells[board_cell] is not None:
                    if board.cells[board_cell].side == board.turn:
                        image_label.setStyleSheet("background-color:#ac6539;")
                        choose_cell_phase = False
                        chosen_cell = board_cell
            else:
                turn = board.make_turn(chosen_cell, board_cell.vertical, board_cell.horizontal)
                if board.turn_phase != 2:
                    if turn is None:
                        buttons[chosen_cell].children()[0].setStyleSheet("background-color:#ba7b55;")
                        choose_cell_phase = True
                        chosen_cell = None
                    elif turn[1] is None:
                        image_label.setStyleSheet("background-color:#ba7b55;")
                        buttons[chosen_cell].children()[0].setStyleSheet("background-color:#ba7b55;")
                        self.update_board(chosen_cell)
                        self.update_board(board_cell)
                        choose_cell_phase = True
                        chosen_cell = None
                        current_turn = board.turn
                        white_sum = board.white_checkers + board.white_kings
                        black_sum = board.black_kings + board.black_checkers
                        while board.turn == current_turn and in_progress:
                            computer_turn = ComputerLogic.make_computer_turn(board)
                            self.update_board(computer_turn[0])
                            self.update_board(computer_turn[1][0])
                            if computer_turn[1][1] is not None:
                                self.update_board(computer_turn[1][1])
                if turn is not None and turn[1] is not None:
                    buttons[chosen_cell].children()[0].setStyleSheet("background-color:#ba7b55;")
                    self.update_board(chosen_cell)
                    self.update_board(turn[1])
                    self.update_board(board_cell)
                    if board.cells[board_cell].side == board.turn:
                        image_label.setStyleSheet("background-color:#ac6539;")
                        chosen_cell = board_cell
                    else:
                        choose_cell_phase = True
                        chosen_cell = None
                        current_turn = board.turn
                        white_sum = board.white_checkers + board.white_kings
                        black_sum = board.black_kings + board.black_checkers
                        while board.turn == current_turn and in_progress:
                            computer_turn = ComputerLogic.make_computer_turn(board)
                            self.update_board(computer_turn[0])
                            self.update_board(computer_turn[1][0])
                            if computer_turn[1][1] is not None:
                                self.update_board(computer_turn[1][1])



    def restart_pressed(self):
        global in_progress
        global chosen_cell
        global choose_cell_phase
        if chosen_cell is not None:
            buttons[chosen_cell].children()[0].setStyleSheet("background-color:#ba7b55;")
            choose_cell_phase = True
            chosen_cell = None
        board.fill_board()
        for cell in board.cells:
            self.update_board(cell)
        self.update_status()
        in_progress = True

    def update_board(self, board_cell: BoardCell):
        checker = board.cells[board_cell]
        group = buttons[board_cell]
        if len(group.children()) > 1:
            group.children()[len(group.children()) - 1].deleteLater()
        if checker is None:
            return
        elif checker.side == Side.BLACK:
            image_label = QtWidgets.QLabel(group)
            image_label.setGeometry(QtCore.QRect(10, 8, 60, 60))
            if checker.is_king:
                image_label.setPixmap(
                    QtGui.QPixmap("C:/Users/User/IdeaProjects/Draughts/src/main/resources/images/Black_king.png"))
            else:
                image_label.setPixmap(
                    QtGui.QPixmap("C:/Users/User/IdeaProjects/Draughts/src/main/resources/images/Black_checker.png"))
            group.children().append(image_label)
            image_label.show()
        else:
            image_label = QtWidgets.QLabel(group)
            image_label.setGeometry(QtCore.QRect(10, 8, 60, 60))
            if checker.is_king:
                image_label.setPixmap(
                    QtGui.QPixmap("C:/Users/User/IdeaProjects/Draughts/src/main/resources/images/White_king.png"))
            else:
                image_label.setPixmap(
                    QtGui.QPixmap("C:/Users/User/IdeaProjects/Draughts/src/main/resources/images/White_checker.png"))
            group.children().append(image_label)
            image_label.show()
        self.update_status()

    def update_status(self):
        global in_progress
        winner = board.winner()
        if winner == Side.BLACK:
            in_progress = False
            status_string = str("Game status:\nBlack wins. Press restart to play again.")
        elif winner == Side.WHITE:
            in_progress = False
            status_string = str("Game status:\nWhite wins. Press restart to play again.")
        elif board.turn == Side.BLACK:
            status_string = str("Game status:\nBlacks turn.")
        else:
            status_string = str("Game status:\nWhites turn.")
        self.label.setText(status_string)

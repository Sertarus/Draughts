# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GameMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!
import functools
import itertools
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QBasicTimer
from PyQt5.QtWidgets import QDialog, QMainWindow

from python.model.Board import Board
from python.model.BoardCell import BoardCell
from python.model.ComputerLogic import ComputerLogic
from python.model.Side import Side

board = Board(8, 8)

buttons = dict()

choose_cell_phase = True

in_progress = False

chosen_cell = None

marked_cells = list()


class QGroupBoxClickable(QtWidgets.QGroupBox):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QGroupBox.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()


class UnclosableDialog(QDialog):
    def keyPressEvent(self, QPressEvent):
        if QPressEvent.key != QtCore.Qt.Key_Escape:
            QPressEvent.accept()


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
        self.restart.pressed.connect(lambda: self.restart_pressed())
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
        self.dialog = UnclosableDialog(self.centralwidget)
        self.dialog.resize(400, 257)
        self.dialog.setMinimumSize(QtCore.QSize(400, 257))
        self.dialog.setMaximumSize(QtCore.QSize(400, 257))
        self.dialog.setModal(True)
        self.dialog.setWindowFlag(Qt.FramelessWindowHint)
        self.dialog.setStyleSheet("QPushButton {\n"
                                  "border-color:black;\n"
                                  "border-style:solid;\n"
                                  "background-color: #dcb35c;\n"
                                  "border-radius: 25px;\n"
                                  "border-width:3px;\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "background-color: #ECE7BC;\n"
                                  "}\n"
                                  "QDialog {\n"
                                  "border-color:black;\n"
                                  "border-style:solid;\n"
                                  "border-width:5px;\n"
                                  "background-color:#FFFACD;\n"
                                  "}\n"
                                  "QFrame {\n"
                                  "border-color:black;\n"
                                  "border-style:solid;\n"
                                  "border-width:3px;\n"
                                  "}\n"
                                  "")
        self.frame = QtWidgets.QFrame(self.dialog)
        self.frame.setGeometry(QtCore.QRect(60, 80, 120, 80))
        self.frame.setStyleSheet("background-color: #dcb35c;\n"
                                 "border-width:3px;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.first_player_human = QtWidgets.QRadioButton(self.frame)
        self.first_player_human.setGeometry(QtCore.QRect(20, 20, 82, 17))
        self.first_player_human.setStyleSheet("border-width:0px;")
        self.first_player_human.setChecked(True)
        self.first_player_computer = QtWidgets.QRadioButton(self.frame)
        self.first_player_computer.setGeometry(QtCore.QRect(20, 50, 82, 17))
        self.first_player_computer.setStyleSheet("border-width:0px;")
        self.frame_2 = QtWidgets.QFrame(self.dialog)
        self.frame_2.setGeometry(QtCore.QRect(220, 80, 120, 80))
        self.frame_2.setStyleSheet("background-color: #dcb35c;\n"
                                   "border-width:3px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.second_player_human = QtWidgets.QRadioButton(self.frame_2)
        self.second_player_human.setGeometry(QtCore.QRect(20, 20, 82, 17))
        self.second_player_human.setStyleSheet("border-width:0px;")
        self.second_player_human.setChecked(True)
        self.second_player_computer = QtWidgets.QRadioButton(self.frame_2)
        self.second_player_computer.setGeometry(QtCore.QRect(20, 50, 82, 17))
        self.second_player_computer.setStyleSheet("border-width:0px;")
        self.push_button = QtWidgets.QPushButton(self.dialog)
        self.push_button.setGeometry(QtCore.QRect(140, 180, 121, 51))
        self.push_button.pressed.connect(lambda: self.dialog_pressed())
        self.dialog_first = QtWidgets.QLabel(self.dialog)
        self.dialog_first.setGeometry(QtCore.QRect(70, 50, 101, 21))
        self.dialog_first.setStyleSheet("font: 75 12pt \"Verdana\";\n"
                                        "border-width:0px;")
        self.dialog_second = QtWidgets.QLabel(self.dialog)
        self.dialog_second.setGeometry(QtCore.QRect(220, 50, 121, 21))
        self.dialog_second.setStyleSheet("font: 75 12pt \"Verdana\";\n"
                                         "border-width:0px;")
        self.dialog.show()
        self.timer = QTimer()
        in_progress = True
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Draughts", "Draughts"))
        self.restart.setText(_translate("MainWindow", "Restart game"))
        self.first_player_human.setText(_translate("Dialog", "Human"))
        self.first_player_computer.setText(_translate("Dialog", "Computer"))
        self.second_player_human.setText(_translate("Dialog", "Human"))
        self.second_player_computer.setText(_translate("Dialog", "Computer"))
        self.push_button.setText(_translate("Dialog", "OK"))
        self.dialog_first.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">First "
                                                       "player</span></p></body></html>"))
        self.dialog_second.setText(_translate("Dialog", "<html><head/><body><p>Second player</p></body></html>"))

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
                        for cell in marked_cells:
                            buttons[cell].children()[0].setStyleSheet("background-color:#ba7b55;")
                            buttons[cell].children()[0].repaint()
                        marked_cells.clear()
                        while board.turn == current_turn and in_progress and (self.first_player_computer.isChecked() or
                                                                              self.second_player_computer.isChecked()):
                            sleep(1)
                            self.make_computer_turn()
                if turn is not None and turn[1] is not None:
                    buttons[chosen_cell].children()[0].setStyleSheet("background-color:#ba7b55;")
                    self.update_board(chosen_cell)
                    self.update_board(turn[1])
                    self.update_board(turn[0])
                    if board.cells[board_cell].side == board.turn:
                        image_label.setStyleSheet("background-color:#ac6539;")
                        chosen_cell = board_cell
                    else:
                        choose_cell_phase = True
                        chosen_cell = None
                        current_turn = board.turn
                        for cell in marked_cells:
                            buttons[cell].children()[0].setStyleSheet("background-color:#ba7b55;")
                            buttons[cell].children()[0].repaint()
                        marked_cells.clear()
                        while board.turn == current_turn and in_progress and (self.first_player_computer.isChecked() or
                                                                              self.second_player_computer.isChecked()):
                            sleep(1)
                            self.make_computer_turn()

    def restart_pressed(self):
        if self.timer.isActive():
            self.timer.stop()
        self.dialog.show()

    def dialog_pressed(self):
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
        for cell in marked_cells:
            buttons[cell].children()[0].setStyleSheet("background-color:#ba7b55;")
            buttons[cell].children()[0].repaint()
        marked_cells.clear()
        in_progress = True
        self.dialog.hide()
        if self.first_player_computer.isChecked() and self.second_player_human.isChecked():
            board.turn = Side.BLACK
            self.make_computer_turn()
        if self.first_player_computer.isChecked() and self.second_player_computer.isChecked():
            self.timer.timeout.connect(lambda: self.make_computer_turn())
            self.timer.start(1500)
        self.update_status()

    def make_computer_turn(self):
        if board.attr_story and board.turn != board.attr_story[len(board.attr_story) - 1][0]:
            for cell in marked_cells:
                buttons[cell].children()[0].setStyleSheet("background-color:#ba7b55;")
                buttons[cell].children()[0].repaint()
            marked_cells.clear()
        computer_turn = ComputerLogic.make_computer_turn(board)
        self.update_board(computer_turn[0])
        self.update_board(computer_turn[1][0])
        buttons[computer_turn[0]].children()[0].setStyleSheet("background-color:#ac6539;")
        buttons[computer_turn[1][0]].children()[0].setStyleSheet("background-color:#ac6539;")
        marked_cells.append(computer_turn[0])
        marked_cells.append(computer_turn[1][0])
        if computer_turn[1][1] is not None:
            self.update_board(computer_turn[1][1])
        if not in_progress and self.timer.isActive():
            self.timer.stop()

    def update_board(self, board_cell: BoardCell):
        checker = board.cells[board_cell]
        group = buttons[board_cell]
        is_inverted_sides = self.first_player_computer.isChecked() and self.second_player_human.isChecked()
        if len(group.children()) > 1:
            group.children()[len(group.children()) - 1].setParent(None)
            group.repaint()
        if checker is None:
            return
        elif (checker.side == Side.BLACK and not is_inverted_sides) or\
                (checker.side == Side.WHITE and is_inverted_sides):
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
        elif (checker.side == Side.WHITE and not is_inverted_sides) or\
                (checker.side == Side.BLACK and is_inverted_sides):
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
        self.centralwidget.repaint()
        self.update_status()

    def update_status(self):
        global in_progress
        winner = board.winner()
        is_inverted_sides = self.first_player_computer.isChecked() and self.second_player_human.isChecked()
        if winner == Side.BLACK:
            in_progress = False
            status_string = str("Game status:\nBlack wins. Press restart to play again.")
        elif winner == Side.WHITE:
            in_progress = False
            status_string = str("Game status:\nWhite wins. Press restart to play again.")
        elif (board.turn == Side.BLACK and not is_inverted_sides) or \
                (board.turn == Side.WHITE and is_inverted_sides) :
            status_string = str("Game status:\nBlacks turn.")
        else:
            status_string = str("Game status:\nWhites turn.")
        self.label.setText(status_string)

from python.model.BoardCell import BoardCell
from python.model.Checker import Checker
from python.model.Side import Side


class Board(object):

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._cells = dict()

    def fillBoard(self):
        self._cells.clear()
        for vertical in range(self._width):
            for horizontal in range(self._height):
                if (vertical + horizontal) % 2 == 0:
                    if horizontal < 3:
                        self._cells[BoardCell(vertical, horizontal)] = Checker(Side.WHITE, False)
                    elif horizontal > 4:
                        self._cells[BoardCell(vertical, horizontal)] = Checker(Side.BLACK, False)
                if BoardCell(vertical, horizontal) not in self._cells:
                    self._cells[BoardCell(vertical, horizontal)] = None

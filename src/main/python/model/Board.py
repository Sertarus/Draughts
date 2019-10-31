from python.model.BoardCell import BoardCell
from python.model.Checker import Checker
from python.model.Side import Side


class Board(object):

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._cells = dict()
        self._turn = Side.WHITE
        self._white_checkers = 0
        self._black_checkers = 0

    def fill_board(self):
        self._cells.clear()
        for vertical in range(self._width):
            for horizontal in range(self._height):
                if (vertical + horizontal) % 2 == 0:
                    if horizontal < 3:
                        self._cells[BoardCell(vertical, horizontal)] = Checker(Side.WHITE, False)
                        self._white_checkers += 1
                    elif horizontal > 4:
                        self._cells[BoardCell(vertical, horizontal)] = Checker(Side.BLACK, False)
                        self._black_checkers += 1
                if BoardCell(vertical, horizontal) not in self._cells:
                    self._cells[BoardCell(vertical, horizontal)] = None

    def make_turn(self, old_cell: BoardCell, vertical: int, horizontal: int):
        turn_cell = BoardCell(vertical, horizontal)
        if 0 <= vertical < self._width and 0 <= horizontal < self._height:
            if self._is_possible_turn(old_cell, turn_cell):
                self._cells[turn_cell] = self._cells[old_cell]
                self._cells[old_cell] = None
                if self._turn == Side.WHITE and horizontal == 0:
                    self._cells[turn_cell].is_king = True
                if self._turn == Side.BLACK and horizontal == self._height - 1:
                    self._cells[turn_cell].is_king = True
                checker_between = self._get_checker_between(old_cell, turn_cell)
                if checker_between is not None:
                    self._cells[checker_between] = None
                return turn_cell
        return None

    def _is_possible_turn(self, old_cell: BoardCell, turn_cell: BoardCell):
        difference = turn_cell.minus(old_cell)
        checker_between = self._get_checker_between(old_cell, turn_cell)
        if self._cells[old_cell].is_king:
            if self._cells[turn_cell] is None and self._get_checker_between(checker_between, turn_cell):
                return True
        else:
            if self._cells[turn_cell] is None:
                if abs(difference.vertical) == 2 and abs(difference.horizontal) == 2:
                    if self._get_checker_between(old_cell, turn_cell).side == self._turn.opposite():
                        return True
                if abs(difference.vertical) == 1 and abs(difference.horizontal) == 1:
                    return True
        return False

    def _get_checker_between(self, old_cell: BoardCell, turn_cell: BoardCell):
        if self._cells[old_cell] is not None:
            if self._cells[old_cell].is_king:
                dist_vertical = old_cell.vertical
                dist_horizontal = old_cell.horizontal
                dif = turn_cell.minus(old_cell)
                direction = BoardCell(0, 0)
                if dif.vertical < 0:
                    direction.vertical = -1
                else:
                    direction.vertical = 1
                if dif.horizontal < 0:
                    direction.horizontal = -1
                else:
                    direction.horizontal = 1
                while 0 <= dist_vertical < self._width and 0 <= dist_horizontal < self._height:
                    for dist_mult in range(max(self._height, self._width)):
                        current_cell = self._cells[old_cell.plus(direction.times(dist_mult))]
                        if current_cell.side == self._turn.opposite():
                            return current_cell
            else:
                dif = BoardCell(turn_cell.minus(old_cell).vertical // 2, turn_cell.minus(old_cell).horizontal // 2)
                cell_between = self._cells[old_cell.plus(dif)]
                if cell_between is not None and cell_between.side == self._turn.opposite():
                    return cell_between
        return None

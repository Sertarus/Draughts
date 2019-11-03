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
        self._turn_phase = 0

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
        possible_turns = dict()
        for key in self._cells:
            if self._cells[key] is not None and self._cells[key].side == self._turn:
                self._else_possible_turns(possible_turns, key)
        if possible_turns:
            self._turn_phase = 1
        if 0 <= vertical < self._width and 0 <= horizontal < self._height and self._cells[old_cell] is not None and \
                self._cells[old_cell].side == self._turn:
            if self._is_possible_turn(old_cell, turn_cell) and \
                    (self._turn_phase == 0 or (old_cell in possible_turns and turn_cell in possible_turns[old_cell])):
                cell_between = self._get_full_cell_between(old_cell, turn_cell)
                self._cells[turn_cell] = self._cells[old_cell]
                self._cells[old_cell] = None
                if self._turn == Side.WHITE and horizontal == self._height - 1:
                    self._cells[turn_cell].is_king = True
                if self._turn == Side.BLACK and horizontal == 0:
                    self._cells[turn_cell].is_king = True
                if cell_between is not None and self._cells[cell_between] is not None:
                    self._cells[cell_between] = None
                    possible_turns = dict()
                    self._else_possible_turns(possible_turns, turn_cell)
                    if possible_turns:
                        self._turn_phase = 1
                        return turn_cell
                    else:
                        self._turn_phase = 0
                self._turn = self._turn.opposite()
                return turn_cell
        return None

    def _is_possible_turn(self, old_cell: BoardCell, turn_cell: BoardCell):
        if self._cells[turn_cell] is None:
            difference = turn_cell.minus(old_cell)
            cell_between = self._get_full_cell_between(old_cell, turn_cell)
            if self._cells[old_cell].is_king:
                if cell_between is None:
                    return True
                if self._cells[cell_between].side != self._turn:
                    second_cell_between = self._get_full_cell_between(cell_between, turn_cell)
                    if self._cells[turn_cell] is None and second_cell_between is None:
                        return True
            else:
                if abs(difference.vertical) == 2 and abs(difference.horizontal) == 2:
                    if cell_between is not None and self._cells[cell_between].side == self._turn.opposite():
                        return True
                if abs(difference.vertical) == 1:
                    if difference.horizontal == 1 and self._turn == Side.WHITE:
                        return True
                    if difference.horizontal == -1 and self._turn == Side.BLACK:
                        return True
        return False

    def _get_full_cell_between(self, old_cell: BoardCell, turn_cell: BoardCell):
        if self._cells[old_cell] is not None:
            if self._cells[old_cell].is_king:
                dist_min_vertical = min(old_cell.vertical, turn_cell.vertical)
                dist_min_horizontal = min(old_cell.horizontal, turn_cell.horizontal)
                dist_max_vertical = max(old_cell.vertical, turn_cell.vertical)
                dist_max_horizontal = max(old_cell.horizontal, turn_cell.horizontal)
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
                for multiplier in range(1, max(self._height, self._width)):
                    current_cell = old_cell.plus(direction.times(multiplier))
                    if current_cell.vertical not in (dist_min_vertical, dist_max_vertical) or \
                            current_cell.horizontal not in (dist_min_horizontal, dist_max_horizontal):
                        break
                    if self._cells[current_cell] is not None:
                        return current_cell
            else:
                dif = BoardCell(turn_cell.minus(old_cell).vertical // 2, turn_cell.minus(old_cell).horizontal // 2)
                cell_between = old_cell.plus(dif)
                if self._cells[cell_between] is not None and self._cells[cell_between].side == self._turn.opposite():
                    return cell_between
        return None

    def _else_possible_turns(self, possible_turns: dict, cell: BoardCell):
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                direction = BoardCell(i, j)
                dir_multiplier = 2
                current_cell = cell.plus(direction.times(dir_multiplier))
                while 0 <= current_cell.vertical < self._width and 0 < current_cell.horizontal < self._height:
                    if self._is_possible_turn(cell, current_cell) and \
                            self._get_full_cell_between(cell, current_cell) is not None:
                        if cell not in possible_turns:
                            possible_turns[cell] = list()
                        possible_turns[cell].append(current_cell)
                    if not self._cells[cell].is_king:
                        break
                    dir_multiplier += 1
                    current_cell = cell.plus(direction.times(dir_multiplier))

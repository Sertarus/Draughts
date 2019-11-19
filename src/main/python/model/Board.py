from python.model.BoardCell import BoardCell
from python.model.Checker import Checker
from python.model.Side import Side


class Board(object):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = dict()
        self.turn = Side.WHITE
        self.white_checkers = 0
        self.white_kings = 0
        self.black_checkers = 0
        self.black_kings = 0
        self.turn_phase = 0
        self.last_beat_cell = None
        self.last_beaten_checker = None
        self.attr_story = list()
        self.fill_board()

    def fill_board(self):
        self.cells.clear()
        self.white_checkers = 0
        self.black_checkers = 0
        self.turn = Side.WHITE
        self.turn_phase = 0
        self.last_beat_cell = None
        for vertical in range(self.width):
            for horizontal in range(self.height):
                if (vertical + horizontal) % 2 != 0:
                    if horizontal < 3:
                        self.cells[BoardCell(vertical, horizontal)] = Checker(Side.BLACK, False)
                        self.black_checkers += 1
                    elif horizontal > 4:
                        self.cells[BoardCell(vertical, horizontal)] = Checker(Side.WHITE, False)
                        self.white_checkers += 1
                if BoardCell(vertical, horizontal) not in self.cells:
                    self.cells[BoardCell(vertical, horizontal)] = None

    def make_turn(self, old_cell: BoardCell, vertical: int, horizontal: int):
        turn_cell = BoardCell(vertical, horizontal)
        possible_turns = dict()
        for key in self.cells:
            if self.cells[key] is not None and self.cells[key].side == self.turn:
                self.else_possible_turns(possible_turns, key)
        if possible_turns and self.turn_phase == 0:
            self.turn_phase = 1
        if 0 <= vertical < self.width and 0 <= horizontal < self.height and self.cells[old_cell] is not None and \
                self.cells[old_cell].side == self.turn:
            if self.is_possible_turn(old_cell, turn_cell) and \
                    (self.turn_phase == 0 or
                     (self.turn_phase == 1 and old_cell in possible_turns and turn_cell in possible_turns[old_cell]) or
                     (self.turn_phase == 2 and self.last_beat_cell in possible_turns)):
                self.attr_story.append((self.turn, self.turn_phase, self.last_beaten_checker, self.last_beat_cell,
                                        self.white_checkers, self.white_kings, self.black_checkers, self.black_kings,
                                        Checker(self.cells[old_cell].side, self.cells[old_cell].is_king)))
                cell_between = self._get_full_cell_between(old_cell, turn_cell)
                self.cells[turn_cell] = self.cells[old_cell]
                self.cells[old_cell] = None
                if self.turn == Side.WHITE and horizontal == 0:
                    self.cells[turn_cell].is_king = True
                    self.white_checkers -= 1
                    self.white_kings += 1
                if self.turn == Side.BLACK and horizontal == self.height - 1:
                    self.cells[turn_cell].is_king = True
                    self.black_checkers -= 1
                    self.black_kings += 1
                if cell_between is not None and self.cells[cell_between] is not None:
                    if self.turn == Side.WHITE:
                        if self.cells[cell_between].is_king:
                            self.black_kings -= 1
                        else:
                            self.black_checkers -= 1
                    else:
                        if self.cells[cell_between].is_king:
                            self.white_kings -= 1
                        else:
                            self.white_checkers -= 1
                    self.last_beaten_checker = self.cells[cell_between]
                    self.cells[cell_between] = None
                    possible_turns = dict()
                    self.else_possible_turns(possible_turns, turn_cell)
                    if possible_turns:
                        self.turn_phase = 2
                        self.last_beat_cell = turn_cell
                        return turn_cell, cell_between
                    else:
                        self.turn_phase = 0
                self.turn = self.turn.opposite()
                return turn_cell, cell_between
        return None

    def unmake_turn(self, old_cell, cell_between, turn_cell):
        self.cells[old_cell] = self.attr_story[len(self.attr_story) - 1][8]
        self.cells[turn_cell] = None
        if cell_between is not None:
            self.cells[cell_between] = self.last_beaten_checker
        self.turn = self.attr_story[len(self.attr_story) - 1][0]
        self.turn_phase = self.attr_story[len(self.attr_story) - 1][1]
        self.last_beaten_checker = self.attr_story[len(self.attr_story) - 1][2]
        self.last_beat_cell = self.attr_story[len(self.attr_story) - 1][3]
        self.white_checkers = self.attr_story[len(self.attr_story) - 1][4]
        self.white_kings = self.attr_story[len(self.attr_story) - 1][5]
        self.black_checkers = self.attr_story[len(self.attr_story) - 1][6]
        self.black_kings = self.attr_story[len(self.attr_story) - 1][7]
        del self.attr_story[-1]

    def winner(self):
        if self.white_checkers == 0 or self._is_side_cant_make_turn(Side.WHITE):
            return Side.BLACK
        if self.black_checkers == 0 or self._is_side_cant_make_turn(Side.BLACK):
            return Side.WHITE
        return None

    def _is_side_cant_make_turn(self, side: Side):
        for cell in self.cells:
            if self.cells[cell] is not None and self.cells[cell].side == side:
                for second_cell in self.cells:
                    dif = cell.minus(second_cell)
                    if abs(dif.horizontal) == abs(dif.vertical):
                        if self.is_possible_turn(cell, second_cell):
                            return False
        return True

    def is_possible_turn(self, old_cell: BoardCell, turn_cell: BoardCell):
        if self.cells[turn_cell] is None:
            difference = turn_cell.minus(old_cell)
            cell_between = self._get_full_cell_between(old_cell, turn_cell)
            if self.cells[old_cell].is_king and abs(difference.vertical) == abs(difference.horizontal):
                if cell_between is None:
                    return True
                if self.cells[cell_between].side != self.turn:
                    second_cell_between = self._get_full_cell_between(cell_between, turn_cell)
                    if self.cells[turn_cell] is None and second_cell_between is None:
                        return True
            else:
                if abs(difference.vertical) == 2 and abs(difference.horizontal) == 2:
                    if cell_between is not None and self.cells[cell_between].side == self.turn.opposite():
                        return True
                if abs(difference.vertical) == 1:
                    if difference.horizontal == -1 and self.turn == Side.WHITE:
                        return True
                    if difference.horizontal == 1 and self.turn == Side.BLACK:
                        return True
        return False

    def _get_full_cell_between(self, old_cell: BoardCell, turn_cell: BoardCell):
        if self.cells[old_cell] is not None:
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
            for multiplier in range(1, max(self.height, self.width)):
                current_cell = old_cell.plus(direction.times(multiplier))
                if current_cell.vertical not in range(dist_min_vertical, dist_max_vertical) or \
                        current_cell.horizontal not in range(dist_min_horizontal, dist_max_horizontal):
                    break
                if self.cells[current_cell] is not None:
                    return current_cell
        return None

    def else_possible_turns(self, possible_turns: dict, cell: BoardCell):
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                direction = BoardCell(i, j)
                dir_multiplier = 2
                current_cell = cell.plus(direction.times(dir_multiplier))
                while 0 <= current_cell.vertical < self.width and 0 <= current_cell.horizontal < self.height:
                    if self.is_possible_turn(cell, current_cell) and \
                            self._get_full_cell_between(cell, current_cell) is not None:
                        if cell not in possible_turns:
                            possible_turns[cell] = list()
                        possible_turns[cell].append(current_cell)
                    if not self.cells[cell].is_king:
                        break
                    dir_multiplier += 1
                    current_cell = cell.plus(direction.times(dir_multiplier))

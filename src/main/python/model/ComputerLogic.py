import sys
from random import randint

from python.model.Board import Board
from python.model.BoardCell import BoardCell
from python.model.Side import Side


class ComputerLogic(object):

    @staticmethod
    def _evaluate(color: Side, board: Board):
        black_value = board.black_checkers * 10 + board.black_kings * 50
        white_value = board.white_checkers * 10 + board.white_kings * 50
        return [white_value - black_value + randint(0, 5), None] if color == Side.WHITE\
            else [black_value - white_value + randint(0, 5), None]

    @staticmethod
    def _generate_all_turns(board: Board):
        turns = []
        possible_turns = dict()
        for key in board.cells:
            if board.cells[key] is not None and board.cells[key].side == board.turn:
                board.else_possible_turns(possible_turns, key)
        for key in board.cells:
            board_checker = board.cells[key]
            if board_checker is not None and board_checker.side == board.turn:
                for i in range(-1, 2, 2):
                    for j in range(-1, 2, 2):
                        direction = BoardCell(i, j)
                        dir_multiplier = 1
                        current_cell = key.plus(direction.times(dir_multiplier))
                        while 0 <= current_cell.vertical < board.width and 0 <= current_cell.horizontal < board.height:
                            if board.is_possible_turn(key, current_cell) and\
                                    (not possible_turns or (key in possible_turns and
                                                            current_cell in possible_turns[key])):
                                turns.append((key, current_cell))
                            if not board_checker.is_king and dir_multiplier == 2:
                                break
                            dir_multiplier += 1
                            current_cell = key.plus(direction.times(dir_multiplier))
        return turns

    @staticmethod
    def _alpha_beta(board: Board, color: Side, depth: int, alpha: int, beta: int, start_color: Side):
        if depth == 0:
            return ComputerLogic._evaluate(start_color, board)
        score = [-sys.maxsize, None]
        turns = ComputerLogic._generate_all_turns(board)
        for turn in turns:
            if score[1] is None:
                score[1] = turn
            turn_properties = board.make_turn(turn[0], turn[1].vertical, turn[1].horizontal)
            if board.turn == color:
                tmp = ComputerLogic._alpha_beta(board, color, depth - 1, alpha, beta, start_color)
            else:
                tmp = ComputerLogic._alpha_beta(board, color.opposite(), depth - 1, -beta, -alpha, start_color)
            board.unmake_turn(turn[0], turn_properties[1], turn[1])
            if tmp[0] > score[0]:
                score[0] = tmp[0]
                score[1] = turn
            if score[0] > alpha:
                alpha = score[0]
            if alpha >= beta:
                return [alpha, None]
        return score

    @staticmethod
    def make_computer_turn(board: Board):
        best_turn = ComputerLogic._alpha_beta(board, board.turn, 6, -sys.maxsize, sys.maxsize, board.turn)
        return best_turn[1][0], board.make_turn(best_turn[1][0], best_turn[1][1].vertical, best_turn[1][1].horizontal)

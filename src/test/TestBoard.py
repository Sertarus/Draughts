import unittest
from python.model.Board import Board
from python.model.BoardCell import BoardCell


class TestBoard(unittest.TestCase):

    test_board = Board(8, 8)

    def testFillBoard(self):
        self.assertEqual(True, not TestBoard.test_board._cells)
        TestBoard.test_board.fill_board()
        self.assertEqual(12, TestBoard.test_board._white_checkers)

    def testMakeTurn(self):
        TestBoard.test_board.fill_board()
        self.assertEqual(None, TestBoard.test_board.make_turn(BoardCell(0, 2), 0, 4))
        self.assertEqual(BoardCell(1, 3), TestBoard.test_board.make_turn(BoardCell(0, 2), 1, 3))
        self.assertEqual(BoardCell(2, 4), TestBoard.test_board.make_turn(BoardCell(3, 5), 2, 4))
        self.assertEqual(BoardCell(3, 5), TestBoard.test_board.make_turn(BoardCell(1, 3), 3, 5))
        self.assertEqual(BoardCell(2, 4), TestBoard.test_board.make_turn(BoardCell(4, 6), 2, 4))
        self.assertEqual(BoardCell(1, 3), TestBoard.test_board.make_turn(BoardCell(2, 2), 1, 3))
        self.assertEqual(None, TestBoard.test_board.make_turn(BoardCell(5, 7), 4, 6))
        self.assertEqual(BoardCell(0, 2), TestBoard.test_board.make_turn(BoardCell(2, 4), 0, 2))
        self.assertEqual(BoardCell(5, 3), TestBoard.test_board.make_turn(BoardCell(6, 2), 5, 3))
        self.assertEqual(BoardCell(4, 6), TestBoard.test_board.make_turn(BoardCell(5, 7), 4, 6))
        self.assertEqual(BoardCell(6, 2), TestBoard.test_board.make_turn(BoardCell(7, 1), 6, 2))
        self.assertEqual(BoardCell(4, 4), TestBoard.test_board.make_turn(BoardCell(5, 5), 4, 4))
        self.assertEqual(BoardCell(3, 5), TestBoard.test_board.make_turn(BoardCell(5, 3), 3, 5))
        self.assertEqual(BoardCell(5, 7), TestBoard.test_board.make_turn(BoardCell(3, 5), 5, 7))
        self.assertEqual(True, TestBoard.test_board._cells[BoardCell(5, 7)].is_king)
        self.assertEqual(BoardCell(3, 5), TestBoard.test_board.make_turn(BoardCell(2, 6), 3, 5))
        self.assertEqual(None, TestBoard.test_board.make_turn(BoardCell(2, 6), 3, 5))
        self.assertEqual(BoardCell(1, 3), TestBoard.test_board.make_turn(BoardCell(5, 7), 1, 3))


if __name__ == '__main__':
    unittest.main()

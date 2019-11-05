import unittest
from python.model.Board import Board
from python.model.BoardCell import BoardCell


class TestBoard(unittest.TestCase):

    test_board = Board(8, 8)

    def testFillBoard(self):
        self.assertEqual(False, not TestBoard.test_board.cells)
        TestBoard.test_board.fill_board()
        self.assertEqual(12, TestBoard.test_board.white_checkers)

    def testMakeTurn(self):
        TestBoard.test_board.fill_board()
        self.assertEqual(None, TestBoard.test_board.make_turn(BoardCell(0, 5), 0, 3))
        self.assertEqual((BoardCell(1, 4), None), TestBoard.test_board.make_turn(BoardCell(0, 5), 1, 4))
        self.assertEqual((BoardCell(2, 3), None), TestBoard.test_board.make_turn(BoardCell(3, 2), 2, 3))
        self.assertEqual((BoardCell(3, 2), BoardCell(2, 3)), TestBoard.test_board.make_turn(BoardCell(1, 4), 3, 2))
        self.assertEqual((BoardCell(2, 3), BoardCell(3, 2)), TestBoard.test_board.make_turn(BoardCell(4, 1), 2, 3))
        self.assertEqual((BoardCell(1, 4), None), TestBoard.test_board.make_turn(BoardCell(2, 5), 1, 4))
        self.assertEqual(None, TestBoard.test_board.make_turn(BoardCell(5, 0), 4, 1))
        self.assertEqual((BoardCell(0, 5), BoardCell(1, 4)), TestBoard.test_board.make_turn(BoardCell(2, 3), 0, 5))
        self.assertEqual((BoardCell(5, 4), None), TestBoard.test_board.make_turn(BoardCell(6, 5), 5, 4))
        self.assertEqual((BoardCell(4, 1), None), TestBoard.test_board.make_turn(BoardCell(5, 0), 4, 1))
        self.assertEqual((BoardCell(6, 5), None), TestBoard.test_board.make_turn(BoardCell(7, 6), 6, 5))
        self.assertEqual((BoardCell(4, 3), None), TestBoard.test_board.make_turn(BoardCell(5, 2), 4, 3))
        self.assertEqual((BoardCell(3, 2), BoardCell(4, 3)), TestBoard.test_board.make_turn(BoardCell(5, 4), 3, 2))
        self.assertEqual((BoardCell(5, 0), BoardCell(4, 1)), TestBoard.test_board.make_turn(BoardCell(3, 2), 5, 0))
        self.assertEqual(True, TestBoard.test_board.cells[BoardCell(5, 0)].is_king)
        self.assertEqual((BoardCell(3, 2), None), TestBoard.test_board.make_turn(BoardCell(2, 1), 3, 2))
        self.assertEqual(None, TestBoard.test_board.make_turn(BoardCell(2, 1), 3, 2))
        self.assertEqual((BoardCell(1, 4), BoardCell(3, 2)), TestBoard.test_board.make_turn(BoardCell(5, 0), 1, 4))
        self.assertEqual((BoardCell(2, 3), BoardCell(1, 4)), TestBoard.test_board.make_turn(BoardCell(0, 5), 2, 3))
        self.assertEqual((BoardCell(5, 4), None), TestBoard.test_board.make_turn(BoardCell(6, 5), 5, 4))
        self.assertEqual((BoardCell(5, 2), None), TestBoard.test_board.make_turn(BoardCell(6, 1), 5, 2))
        self.assertEqual((BoardCell(2, 5), None), TestBoard.test_board.make_turn(BoardCell(3, 6), 2, 5))
        self.assertEqual((BoardCell(2, 1), None), TestBoard.test_board.make_turn(BoardCell(3, 0), 2, 1))
        self.assertEqual((BoardCell(3, 6), None), TestBoard.test_board.make_turn(BoardCell(4, 7), 3, 6))
        self.assertEqual((BoardCell(3, 2), None), TestBoard.test_board.make_turn(BoardCell(2, 1), 3, 2))
        self.assertEqual((BoardCell(7, 6), None), TestBoard.test_board.make_turn(BoardCell(6, 7), 7, 6))
        self.assertEqual((BoardCell(4, 3), None), TestBoard.test_board.make_turn(BoardCell(5, 2), 4, 3))
        self.assertEqual((BoardCell(0, 5), None), TestBoard.test_board.make_turn(BoardCell(1, 6), 0, 5))
        self.assertEqual((BoardCell(6, 5), BoardCell(5, 4)), TestBoard.test_board.make_turn(BoardCell(4, 3), 6, 5))
        self.assertEqual((BoardCell(4, 7), BoardCell(5, 6)), TestBoard.test_board.make_turn(BoardCell(6, 5), 4, 7))
        self.assertEqual(True, TestBoard.test_board.turn_phase == 0)


if __name__ == '__main__':
    unittest.main()

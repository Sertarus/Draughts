import unittest
from python.model.BoardCell import BoardCell


class TestBoardCell(unittest.TestCase):

    first_board_cell = BoardCell(1, 3)
    second_board_cell = BoardCell(2, 1)
    first_board_cell_copy = BoardCell(1, 3)

    def testGetVertical(self):
        self.assertEqual(1, TestBoardCell.first_board_cell.vertical)

    def testGetHorizontal(self):
        self.assertEqual(3, TestBoardCell.first_board_cell.horizontal)

    def testSetHorizontal(self):
        test = BoardCell(1, 1)
        test.horizontal = 2
        self.assertEqual(2, test.horizontal)
        test.__horizontal = ""
        self.assertEqual(2, test.horizontal)

    def testPlus(self):
        self.assertEqual(BoardCell(3, 4), TestBoardCell.first_board_cell.plus(TestBoardCell.second_board_cell))

    def testMinus(self):
        self.assertEqual(BoardCell(-1, 2), TestBoardCell.first_board_cell.minus(TestBoardCell.second_board_cell))

    def testTimes(self):
        self.assertEqual(BoardCell(2, 6), TestBoardCell.first_board_cell.times(2))

    def testEqual(self):
        self.assertFalse(TestBoardCell.first_board_cell.__eq__(TestBoardCell.second_board_cell))
        self.assertTrue(TestBoardCell.first_board_cell.__eq__(TestBoardCell.first_board_cell_copy))


if __name__ == '__main__':
    unittest.main()

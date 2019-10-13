import unittest
from python.model.BoardCell import BoardCell


class TestBoardCell(unittest.TestCase):

    firstBoardCell = BoardCell(1, 3)
    secondBoardCell = BoardCell(2, 1)
    firstBoardCellCopy = BoardCell(1, 3)

    def testGetVertical(self):
        self.assertEqual(1, TestBoardCell.firstBoardCell.vertical)

    def testGetHorizontal(self):
        self.assertEqual(3, TestBoardCell.firstBoardCell.horizontal)

    def testSetHorizontal(self):
        test = BoardCell(1, 1)
        test.horizontal = 2
        self.assertEqual(2, test.horizontal)
        test.__horizontal = ""
        self.assertEqual(2, test.horizontal)

    def testPlus(self):
        self.assertEqual(BoardCell(3, 4), TestBoardCell.firstBoardCell.plus(TestBoardCell.secondBoardCell))

    def testMinus(self):
        self.assertEqual(BoardCell(-1, 2), TestBoardCell.firstBoardCell.minus(TestBoardCell.secondBoardCell))

    def testTimes(self):
        self.assertEqual(BoardCell(2, 6), TestBoardCell.firstBoardCell.times(2))

    def testEqual(self):
        self.assertFalse(TestBoardCell.firstBoardCell.__eq__(TestBoardCell.secondBoardCell))
        self.assertTrue(TestBoardCell.firstBoardCell.__eq__(TestBoardCell.firstBoardCellCopy))


if __name__ == '__main__':
    unittest.main()

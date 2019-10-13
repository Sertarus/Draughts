import unittest

from python.model.Checker import Checker
from python.model.Side import Side


class TestChecker(unittest.TestCase):

    def test_side(self):
        test = Checker(Side.WHITE, False)
        self.assertEqual(Side.WHITE, test.side)
        self.assertFalse(test.is_king)
        test.side = Side.BLACK
        test.is_king = True
        self.assertEqual(Side.BLACK, test.side)
        self.assertTrue(test.is_king)


if __name__ == '__main__':
    unittest.main()

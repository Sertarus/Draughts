import unittest
from python.model.Side import Side


class TestSide(unittest.TestCase):

    def test_opposite(self):
        self.assertEqual(Side.BLACK, Side.WHITE.opposite())


if __name__ == '__main__':
    unittest.main()

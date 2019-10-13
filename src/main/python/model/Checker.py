from python.model.Side import Side


class Checker(object):

    def __init__(self, side, is_king: bool):
        try:
            if isinstance(side, Side):
                self._side = side
                self._is_king = is_king
        except ValueError:
            print('Incorrect side')

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, side):
        if isinstance(side, Side):
            self._side = side

    @property
    def is_king(self):
        return self._is_king

    @is_king.setter
    def is_king(self, is_king: bool):
        self._is_king = is_king

class BoardCell(object):

    def __init__(self, vertical: int, horizontal: int):
        self._vertical = vertical
        self._horizontal = horizontal

    @property
    def vertical(self):
        return self._vertical

    @vertical.setter
    def vertical(self, value: int):
        self._vertical = value

    @property
    def horizontal(self):
        return self._horizontal

    @horizontal.setter
    def horizontal(self, value: int):
        self._horizontal = value

    def plus(self, other):
        return BoardCell(self._vertical + other._vertical, self._horizontal + other._horizontal)

    def minus(self, other):
        return BoardCell(self._vertical - other._vertical, self._horizontal - other._horizontal)

    def times(self, multiplier):
        return BoardCell(self._vertical * multiplier, self._horizontal * multiplier)

    def _attrs(self):
        return self._vertical, self._horizontal

    def __eq__(self, other):
        return isinstance(other, BoardCell) and self._attrs() == other._attrs()

    def __hash__(self):
        return (13 * 17 + self._vertical) * 37 + self._horizontal

    def __repr__(self):
        return "%d %d" % (self._vertical, self._horizontal)

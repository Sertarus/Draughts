from enum import Enum


class Side(Enum):

    WHITE = 1
    BLACK = 2

    def opposite(self):
        if self == Side.WHITE:
            return Side.BLACK
        else:
            return Side.WHITE

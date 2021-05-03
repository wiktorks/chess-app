import numpy as np
from Pawn import ChessEntity, Pawn

class ChessBoard:
    def __init__(self):
        self.chessboard = np.array([None for _ in range(64)], dtype=ChessEntity).reshape(8, 8)
        self.chessboard[7, 1] = Pawn(7, 1)


if __name__ == '__main__':
    a = np.array([None for _ in range(64)], dtype=Pawn).reshape(8, 8)
    a[7, 1] = Pawn(7, 1, 'Black')
    print(a[7, 1].color)
import numpy as np
import Pieces as piece_module


class ChessError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ChessBoard:
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def __init__(self):
        Piece = piece_module.Piece
        Pawn = piece_module.Pawn
        self.chess_fields = {}
        for i in range(8):
            for j in range(8):
                self.chess_fields[f'{self.letters[i]}{j + 1}'] = (i, j)

        self.chessboard = np.array(
            [None for _ in range(64)], dtype=Piece).reshape(8, 8)
        for i in range(8):
            self.chessboard[i, 1] = Pawn(i, 1, 'W')

        for i in range(8):
            self.chessboard[i, 6] = Pawn(i, 6, 'B')

        piece_kinds = ['Rook', 'Knight', 'Bishop', 'Queen', 'King']

        for i, piece_kind in enumerate(piece_kinds):
            piece = getattr(piece_module, piece_kind)
            self.chessboard[i, 0] = piece(i, 0, 'W')
            self.chessboard[i, 7] = piece(i, 7, 'B')

            if i < 3:
                self.chessboard[7 - i, 0] = piece(7-i, 0, 'W')
                self.chessboard[7 - i, 7] = piece(7-i, 7, 'B')

    def print_board(self):
        def print_border():
            print(' ', end='')
            [print('+---', end='') for _ in range(8)]
            print('+')

        for x in range(8):
            print_border()
            print(f'{self.letters[x]}', end='')
            for y in range(8):
                if self.chessboard[x, y]:
                    print(f'| {str(self.chessboard[x, y])} ', end='')
                else:
                    print('|   ', end='')
            print('|')

        print_border()
        print(f'   {"".join([f"{i}   " for i in range(1, 9)])}')

    def get_player_move(self, turn):
        while True:
            try:
                player_input = input('Select the piece and place you want to move it (eg. F0 E3).\nType "board" to display board on console: ')
                player_move = player_input.split(' ')[:2]

                if len(player_move) < 2:
                    raise ChessError('>Please give two arguments separated by space.')
                if not set(player_move).issubset(self.chess_fields.keys()):
                    raise ChessError('>First value should be between A and H and second between 1 and 8.')

                piece, move = player_move
                piece = self.chessboard[self.chess_fields[piece]]
                if not piece or (isinstance(piece, piece_module.Piece) and piece.color != turn):
                    raise ChessError('>Please select the piece of Your color.')
                
                moves, attacks = piece.get_available_moves(self.chessboard)
                if self.chess_fields[move] not in moves + attacks:
                    raise ChessError('>Illegal move')

                return piece, self.chess_fields[move]

            except ChessError as chess_error:
                print(chess_error)


    def game(self):
        turn = 'W'
        print('--------------Chess Terminal game------------')
        print('For board display type "board" in console')
        while True:
            print('White turn') if turn == 'W' else print('Black turn')
            self.print_board()

            piece, move = self.get_player_move(turn)

            self.chessboard[move] = piece
            self.chessboard[piece.get_position()] = None
            piece.move(move)

            turn = 'B' if turn == 'W' else 'W'


if __name__ == '__main__':
    board = ChessBoard()
    board.game()

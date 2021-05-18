import numpy as np
# from Pawn import Piece, Pawn, Bishop, Knight, Rook, King, Queen
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

# popraw rozmieszczenie pionów ( w pętli)
        # piece_module = importlib.import_module('Pawn')
        piece_kinds = ['Rook', 'Knight', 'Bishop', 'Queen', 'King']

        for i, piece_kind in enumerate(piece_kinds):
            piece = getattr(piece_module, piece_kind)
            self.chessboard[i, 0] = piece(i, 0, 'W')
            self.chessboard[i, 7] = piece(i, 7, 'B')

            if i < 3:
                self.chessboard[7 - i, 0] = piece(7-i, 0, 'W')
                self.chessboard[7 - i, 7] = piece(7-i, 7, 'B')


    def print_board(self):
        for x in range(8):
            print(f'{self.letters[x]}[ ', end='')
            for y in range(8):
                if self.chessboard[x, y]:
                    print(f'{str(self.chessboard[x, y])} ', end='')
                else:
                    print('O ', end='')
            print(']')
        print(f'X[ {"".join([f"{i} " for i in range(1, 9)])}]')

    # Ogranicz niepotrzebne pętle w wyborze pionów
    def get_player_move(self, input_message, turn, selected_pawn=None):
        while True:
            player_input = input(input_message)
            if player_input == 'board':
                self.print_board()
            elif selected_pawn and player_input == 'cancel':
                return player_input
            else:
                try:
                    # Spróbuj ze słownikiem pól szachownicy: {"A1": (0, 0), ...}
                    coordinates = player_input.split(' ')[:2]
                    if coordinates[0].upper() not in self.letters or int(coordinates[1]) not in range(1, 9):
                        raise ChessError(
                            'First value must be letter from A to H and second value must be integer from 1 to 8')

                    coordinates = self.letters.index(
                        coordinates[0].upper()), int(coordinates[1]) - 1
                    # {
                    # "A1" : (0,0) 
                    # }
                    if selected_pawn:
                        moves, attacks = selected_pawn.get_available_moves(
                            self.chessboard)
                        if coordinates not in moves and coordinates not in attacks:
                            raise ChessError('Illegal move')
                    else:
                        temp_piece = self.chessboard[coordinates]
                        if not temp_piece or temp_piece.color != turn:
                            raise ChessError('Choose a figure of your color.')

                    return coordinates
                except ChessError as chessErr:
                    print(chessErr)

    def game(self):
        turn = 'W'
        print('--------------Chess Terminal game------------')
        print('For board display type "board" in console')
        while True:
            print('White turn') if turn == 'W' else print('Black turn')
            self.print_board()

            while True:
                piece_coordinates = self.get_player_move(
                    'Select the piece you want to move. Type "board" in console to display chessboard\n',
                    turn
                )
                piece = self.chessboard[piece_coordinates]
                move_coordinates = self.get_player_move(
                    'Select place you want your piece to move. Type "board" in console to display chessboard.\nType "cancel" to deselect the piece.\n',
                    turn,
                    selected_pawn=piece
                )
                if move_coordinates != 'cancel':
                    break

            old_position = piece.x, piece.y

            self.chessboard[move_coordinates] = piece
            self.chessboard[old_position] = None
            piece.move(move_coordinates)

            turn = 'B' if turn == 'W' else 'W' 


if __name__ == '__main__':
    board = ChessBoard()
    board.game()
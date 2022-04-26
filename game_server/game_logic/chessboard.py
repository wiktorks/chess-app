from copy import deepcopy
import numpy as np
from game_logic.pieces import Piece, Pawn, Queen, King, Rook, Bishop, Knight
from utils.errors import ChessError

# TODO: Poprawić roszadę, dodać bicie z przelotem.
# Zamiast * lepiej wylistować wszystkie rzeczy z modułu (wydajniej)


class ChessBoard:
    """Main class for chess game"""

    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    turn = "W"

    def __init__(self):
        # Piece = Piece
        # Pawn = Pawn
        self.chess_fields = {}

        # wrzuć do funkcji tworzenie szachownicy

        for i in range(8):
            for j in range(8):
                self.chess_fields[f"{self.letters[i]}{j + 1}"] = (i, j)

        self.chessboard = np.array([None for _ in range(64)], dtype=Piece).reshape(8, 8)
        for i in range(8):
            self.chessboard[i, 1] = Pawn(i, 1, "W")
            self.chessboard[i, 6] = Pawn(i, 6, "B")

        # for i in range(8):

        piece_kinds = ["Rook", "Knight", "Bishop", "Queen", "King"]

        for i, piece_kind in enumerate(piece_kinds):
            piece = eval(f"{piece_kind}")
            self.chessboard[i, 0] = piece(i, 0, "W")
            self.chessboard[i, 7] = piece(i, 7, "B")

            if i < 3:
                self.chessboard[7 - i, 0] = piece(7 - i, 0, "W")
                self.chessboard[7 - i, 7] = piece(7 - i, 7, "B")

            if i == 4:
                self.kings = {"W": self.chessboard[i, 0], "B": self.chessboard[i, 7]}
        # ------

    def get_board(self):
        """returns chessboard in form of Python list"""
        return [str(x) for x in self.chessboard.tolist()]
        # return list(map(lambda x: str(x), self.chessboard.tolist()))

    def print_board(self):
        """Prints board to standard output"""
        chessboard = np.flip(np.copy(self.chessboard), axis=1).transpose()
        border = f'  {"+---"*8}+'
        for x in range(8):
            print(border)
            print(f"{8 - x} ", end="")
            for y in range(8):
                if chessboard[x, y]:
                    print(f"| {str(chessboard[x, y])} ", end="")
                else:
                    print("|   ", end="")
            print("|")

        print(border)
        print(f'    {"".join([f"{self.letters[i]}   " for i in range(8)])}')

    def get_piece_object(self, field):
        """Retrieves piece objects from the given chessboard field

        Args:
            field (string): argument resembling chess field (like "H1" etc.)

        Raises:
            ChessError: 'Attribute must be a string resembling chess field (like "H1" etc.)'
            ChessError: Piece not found on given chess field:
            ChessError: Piece must be the same color of the player.

        Returns:
            Piece: object of type Piece selected by the given coordinates
        """
        if field not in self.chess_fields:
            raise ChessError(
                'Attribute must be a string resembling chess field (like "H1" etc.)'
            )

        piece = self.chessboard[self.chess_fields[field]]
        if not piece:
            raise ChessError(f"Piece not found on given chess field: {field}")

        if self.turn != piece.color:
            raise ChessError("Piece must be the same color of the player.")

        return piece

    def get_available_moves(self, piece, enemy_turn=False):
        """_summary_

        Args:
            piece (_type_): _description_
            enemy_turn (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        if not isinstance(piece, Piece):
            piece = self.get_piece_object(piece)

        moves = piece.get_moves(self.chessboard)

        king = (
            deepcopy(self.kings["W" if self.turn == "B" else "B"])
            if enemy_turn
            else deepcopy(self.kings[self.turn])
        )

        def filter_check_moves(move):
            chessboard_copy = np.copy(self.chessboard)
            chessboard_copy[move["move"]] = piece
            chessboard_copy[piece.get_position()] = None
            if str(piece) in ["k", "K"]:
                king.move(move["move"])

            return not king.is_check(chessboard_copy)

        return list(filter(filter_check_moves, moves))

    def move_piece(self, piece, move):
        """_summary_

        Args:
            piece (_type_): _description_
            move (_type_): _description_

        Raises:
            ChessError: _description_
        """
        chess_piece = (
            piece if isinstance(piece, Piece) else self.get_piece_object(piece)
        )
        chess_move = self.chess_fields[move]

        available_moves = self.get_available_moves(chess_piece)
        chess_move = list(
            filter(
                lambda available_move: available_move["move"] == chess_move,
                available_moves,
            )
        )

        if not chess_move:
            raise ChessError("Illegal move")

        chess_move = chess_move.pop()
        if chess_move["type"] == "castling-long":
            self.chessboard[chess_piece.x, 2] = chess_piece
            self.chessboard[chess_piece.get_position()] = None
            rook = self.chessboard[chess_piece.x, 0]
            self.chessboard[chess_piece.x, 3] = rook
            self.chessboard[rook.get_position()] = None
            rook.move(chess_piece.x, 3)

        elif chess_move["type"] == "castling-short":
            self.chessboard[6, chess_piece.y] = chess_piece
            self.chessboard[chess_piece.get_position()] = None
            chess_piece.move((6, chess_piece.y))
            rook = self.chessboard[7, chess_piece.y]
            self.chessboard[5, chess_piece.y] = rook
            self.chessboard[rook.get_position()] = None
            rook.move((5, chess_piece.y))

        else:
            self.chessboard[tuple(chess_move["move"])] = chess_piece
            self.chessboard[chess_piece.get_position()] = None
            chess_piece.move(tuple(chess_move["move"]))

        if str(chess_piece) == "K":
            self.kings[self.turn] = chess_piece

        self.turn = "B" if self.turn == "W" else "W"

    def get_game_status(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        status = {}

        check = False
        enemy_king = self.kings["B" if self.turn == "W" else "W"]
        if enemy_king.is_check(self.chessboard):
            check = True

        status["isCheck"] = check

        end_game = False
        for row in self.chessboard:
            for field in row:
                if isinstance(field, Piece) and field.color != self.turn:
                    moves = self.get_available_moves(field, enemy_turn=True)
                    if moves:
                        break
            else:
                continue

            break
        else:
            end_game = True

        status["endGame"] = end_game
        if end_game:
            status["winner"] = self.turn if check else "stalemate"

        return status

    # -------------------------------------------
    def get_player_move_input(self):
        """_summary_

        Raises:
            ChessError: _description_
            ChessError: _description_
            ChessError: _description_
            ChessError: _description_

        Returns:
            _type_: _description_
        """
        invalid_move = True

        while invalid_move:
            try:
                player_input = input(
                    'Select the piece and place you want to move it (eg. G1 F3).\nType "board" to display board on console: '
                )

                if player_input == "board":
                    self.print_board()
                    continue

                player_move = player_input.split(" ")[:2]

                if len(player_move) < 2:
                    raise ChessError(">Please give two arguments separated by space.")

                if not set(player_move).issubset(self.chess_fields.keys()):
                    raise ChessError(
                        ">First value should be between A and H and second between 1 and 8."
                    )

                piece_coordinates, move = player_move
                piece = self.chessboard[self.chess_fields[piece_coordinates]]
                if not piece or (isinstance(piece, Piece) and piece.color != self.turn):
                    raise ChessError(">Please select the piece of Your color.")

                available_moves = self.get_available_moves(piece)
                move = [
                    m for m in available_moves if self.chess_fields[move] == m["move"]
                ]
                if not move:
                    raise ChessError(">Illegal move")

                invalid_move = False

            except ChessError as chess_error:
                print(chess_error)

        return piece, move.pop()

    def local_terminal_game(self):
        """_summary_

        Raises:
            ChessError: _description_
        """
        print("--------------Chess Terminal game--------------")
        while True:
            if self.turn == "W":
                print("White turn")
            else:
                print("Black turn")

            self.print_board()

            piece, move = self.get_player_move_input()
            chess_move = f"{self.letters[move['move'][0]]}{move['move'][1] + 1}"
            self.move_piece(piece, chess_move)
            status = self.get_game_status()
            if status["isCheck"]:
                if status["endGame"]:
                    print(f"Game Over. The winner is: {status['winner']}")
                    break
                print(f"{self.turn} Check!")

            # self.turn = "B" if self.turn == "W" else "W"
            self.turn = "B" if self.turn == "W" else "W"

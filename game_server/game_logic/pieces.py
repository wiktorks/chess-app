from itertools import product, permutations
import numpy as np

# formatter black


class Piece:
    """Base class for all chessboard pieces"""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.start_position = True

    def check_move(self, move):
        """Check if given move is within bounds of chessboard"""

        x, y = move
        if x in range(0, 8) and y in range(0, 8):
            return True

        return False

    def move(self, move):
        """Assign new chessboard coordinates for piece"""

        if not self.check_move(move):
            raise ValueError("x should be between 0 and 7")

        self.x, self.y = move
        self.start_position = False

    def get_position(self):
        """Returns (x, y) position tuple"""

        return (self.x, self.y)

    def check_diagonal(self, direction, chessboard):
        """Returns list of available moves on diagonal from given direction"""

        available_moves = []
        position = np.array([self.x, self.y], dtype=int) + direction

        while np.all(position >= 0) and np.all(position < 8):
            if self.check_move(tuple(position)):
                if chessboard[tuple(position)] is None:
                    available_moves.append({"type": "move", "move": tuple(position)})
                    position += direction

                else:
                    if (
                        isinstance(chessboard[tuple(position)], Piece)
                        and chessboard[tuple(position)].color != self.color
                    ):
                        available_moves.append(
                            {"type": "attack", "move": tuple(position)}
                        )
                    break

        return available_moves


class Pawn(Piece):
    """Pawn class responsible for Pawn movement logic on chessboard

    Args:
        Piece (_type_): _description_
    """

    def get_moves(self, chessboard):
        """_summary_

        Args:
            chessboard (numpy 2d array): 2D numpy array chessboard size

        Returns:
            list: all available moves for pawn
        """
        available_moves = []

        direction = 1 if self.color == "W" else -1

        if (
            self.check_move((self.x, self.y + direction))
            and not chessboard[(self.x, self.y + direction)]
        ):
            available_moves.append(
                {"type": "move", "move": (self.x, self.y + direction)}
            )

        if (
            self.start_position
            and self.check_move((self.x, self.y + direction * 2))
            and not chessboard[(self.x, self.y + direction * 2)]
        ):
            available_moves.append(
                {"type": "move", "move": (self.x, self.y + direction * 2)}
            )

        for attack in [
            (self.x + 1, self.y + direction),
            (self.x - 1, self.y + direction),
        ]:
            if self.check_move(attack) and chessboard[attack]:
                available_moves.append({"type": "attack", "move": attack})

        return available_moves

    def __repr__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return "P" if self.color == "W" else "p"


class Bishop(Piece):
    """_summary_

    Args:
        Piece (_type_): _description_
    """

    def get_moves(self, chessboard):
        """_summary_

        Args:
            chessboard (_type_): _description_

        Returns:
            _type_: _description_
        """
        available_moves = []

        for direction in list(product([-1, 1], [-1, 1])):
            moves = self.check_diagonal(direction, chessboard)
            if moves:
                available_moves += moves

        return available_moves

    def __repr__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return "B" if self.color == "W" else "b"


class Knight(Piece):
    """_summary_

    Args:
        Piece (_type_): _description_
    """

    def get_moves(self, chessboard):
        """_summary_

        Args:
            chessboard (_type_): _description_

        Returns:
            _type_: _description_
        """
        available_moves = []
        current_position = np.array([self.x, self.y], dtype=int)

        for direction in filter(
            lambda x: abs(x[0]) != abs(x[1]), permutations([-1, -2, 1, 2], 2)
        ):
            # [
            #     [2, 1],
            #     [2, -1],
            #     [-2, 1],
            #     [-2, -1],
            #     [1, 2],
            #     [1, -2],
            #     [-1, 2],
            #     [-1, -2],
            # ]:
            next_position = current_position + direction
            if self.check_move(tuple(next_position)):
                piece = chessboard[tuple(next_position)]

                if piece is None:
                    available_moves.append(
                        {"type": "move", "move": tuple(next_position)}
                    )

                elif isinstance(piece, Piece) and piece.color != self.color:
                    available_moves.append(
                        {"type": "attack", "move": tuple(next_position)}
                    )

        return available_moves

    def __repr__(self):
        return "H" if self.color == "W" else "h"


class Rook(Piece):
    """_summary_

    Args:
        Piece (_type_): _description_
    """

    def get_moves(self, chessboard):
        """_summary_

        Args:
            chessboard (_type_): _description_

        Returns:
            _type_: _description_
        """
        available_moves = []

        for direction in [[0, 1], [0, -1], [-1, 0], [1, 0]]:
            moves = self.check_diagonal(direction, chessboard)
            if moves:
                available_moves += moves
            # if attacks:
            #     available_attacks += attacks

        return available_moves

    def __repr__(self):
        return "R" if self.color == "W" else "r"


class King(Piece):
    """_summary_

    Args:
        Piece (_type_): _description_
    """

    def is_check(self, chessboard):
        """_summary_

        Args:
            chessboard (_type_): _description_

        Returns:
            _type_: _description_
        """
        current_position = np.array(self.get_position(), dtype=int)
        all_attacks = []
        for direction in [
            [0, 1],
            [0, -1],
            [-1, 0],
            [1, 0],
            [1, 1],
            [1, -1],
            [-1, -1],
            [-1, 1],
        ]:
            attacks = list(
                filter(
                    lambda move: move["type"] == "attack",
                    self.check_diagonal(direction, chessboard),
                )
            )
            all_attacks += attacks

        if all_attacks:
            for position in all_attacks:
                piece = chessboard[position["move"]]
                piece_attacks = list(
                    filter(
                        lambda move: move["type"] == "attack",
                        piece.get_moves(chessboard),
                    )
                )
                if self.get_position() in (attack["move"] for attack in piece_attacks):
                    return True

        for next_position in [
            [2, 1],
            [2, -1],
            [-2, 1],
            [-2, -1],
            [1, 2],
            [1, -2],
            [-1, 2],
            [-1, -2],
        ]:
            move = tuple(current_position + next_position)

            if self.check_move(move):
                piece = chessboard[move]
                if str(piece) in ["h", "H"] and piece.color != self.color:
                    return True

        return False

    def get_moves(self, chessboard):
        """_summary_

        Args:
            chessboard (_type_): _description_

        Returns:
            _type_: _description_
        """
        moves = []
        current_position = np.array([self.x, self.y], dtype=int)

        for direction in [
            [0, 1],
            [0, -1],
            [-1, 0],
            [1, 0],
            [1, 1],
            [1, -1],
            [-1, -1],
            [-1, 1],
        ]:
            next_position = tuple(current_position + direction)

            if self.check_move(next_position):
                if chessboard[next_position] is None:
                    moves.append({"type": "move", "move": next_position})

                elif (
                    isinstance(chessboard[next_position], Piece)
                    and chessboard[next_position].color != self.color
                ):
                    moves.append({"type": "attack", "move": next_position})

        if self.start_position and not self.is_check(chessboard):
            rook_l = chessboard[0, self.y]
            rook_r = chessboard[7, self.y]

            if (
                isinstance(rook_l, Rook)
                and rook_l.color == self.color
                and rook_l.start_position
            ):
                castling = True
                for i in [2, 3]:
                    if chessboard[i, self.y]:
                        castling = False
                        break
                    else:
                        chessboard_copy = np.array(chessboard)
                        king_position = King(i, self.y, self.color)
                        chessboard_copy[i, self.y] = king_position

                        if king_position.is_check(chessboard_copy):
                            castling = False
                            break
                if castling:
                    moves.append({"type": "castling-long", "move": (2, self.y)})

            if (
                isinstance(rook_r, Rook)
                and rook_r.color == self.color
                and rook_r.start_position
            ):
                castling = True
                for i in [5, 6]:
                    if chessboard[i, self.y]:
                        castling = False
                        break
                    else:
                        chessboard_copy = np.array(chessboard)
                        king_position = King(i, self.y, self.color)
                        chessboard_copy[i, self.y] = king_position

                        if king_position.is_check(chessboard_copy):
                            castling = False
                            break

                if castling:
                    moves.append({"type": "castling-short", "move": (6, self.y)})

        return moves

    def __repr__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return "K" if self.color == "W" else "k"


class Queen(Piece):
    """_summary_

    Args:
        Piece (_type_): _description_
    """

    def get_moves(self, chessboard):
        """_summary_

        Args:
            chessboard (_type_): _description_

        Returns:
            _type_: _description_
        """
        available_moves = []

        for direction in [
            [0, 1],
            [0, -1],
            [-1, 0],
            [1, 0],
            [1, 1],
            [1, -1],
            [-1, -1],
            [-1, 1],
        ]:
            moves = self.check_diagonal(direction, chessboard)
            if moves:
                available_moves += moves

        return available_moves

    def __repr__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return "Q" if self.color == "W" else "q"

import numpy as np


class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.start_position = True

    def move(self, move):
        for x in move:
            if x not in range(0, 8):
                raise ValueError('x should be between 0 and 7')

        self.x, self.y = move
        self.start_position = False

    
    def check_move(self, move):
        x, y = move
        if x >= 0 and y >= 0 and x < 8 and y < 8:
            return True

        return False

    def get_position(self):
        return (self.x, self.y)

    def check_diagonal(self, direction, chessboard):
        available_moves = []
        available_attacks = []
        position = np.array([self.x, self.y]) + direction

        while np.all(position >= 0) and np.all(position < 8):
            if self.check_move(tuple(position)):
                if chessboard[tuple(position)] == None:
                    available_moves.append(tuple(position))
                    position += direction

                else:
                    if isinstance(chessboard[tuple(position)], Piece) and chessboard[tuple(position)].color != self.color:
                        available_attacks.append(tuple(position))
                    break

        return available_moves, available_attacks



class Pawn(Piece):
    def get_moves(self, chessboard):
        available_moves = []
        available_attacks = []

        direction = 1 if self.color == 'W' else -1

        if self.check_move((self.x, self.y + direction)) and not chessboard[(self.x, self.y + direction)]:
            available_moves.append((self.x, self.y + direction))

        if self.start_position and self.check_move((self.x, self.y + direction * 2)) and not chessboard[(self.x, self.y + direction * 2)]:
            available_moves.append((self.x, self.y + direction * 2))

        for attack in [(self.x + 1, self.y + direction), (self.x - 1, self.y + direction)]:
            if self.check_move(attack) and chessboard[attack]:
                available_attacks.append(attack)

        return available_moves, available_attacks

    def __str__(self):
        return 'P' if self.color == 'W' else 'p'


class Bishop(Piece):
    def get_moves(self, chessboard):
        available_moves = []
        available_attacks = []

        for direction in [[1, 1], [1, -1], [-1, -1], [-1, 1]]:
            moves, attacks = self.check_diagonal(direction, chessboard)
            if moves:
                available_moves += moves
            if attacks:
                available_attacks += attacks

        return available_moves, available_attacks

    def __str__(self):
        return 'B' if self.color == 'W' else 'b'


class Knight(Piece):
    def get_moves(self, chessboard):
        available_moves = []
        available_attacks = []
        current_position = np.array([self.x, self.y])

        for direction in [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]:
            next_position = current_position + direction
            if self.check_move(tuple(next_position)):
                piece = chessboard[tuple(next_position)]
                if chessboard[tuple(next_position)] == None:
                    available_moves.append(tuple(next_position))
                    # (2, 6)
                elif isinstance(chessboard[tuple(next_position)], Piece) and chessboard[tuple(next_position)].color != self.color:
                    available_attacks.append(tuple(next_position))

        return available_moves, available_attacks

    def __str__(self):
        return 'H' if self.color == 'W' else 'h'


class Rook(Piece):
    def get_moves(self, chessboard):
        available_moves = []
        available_attacks = []

        for direction in [[0, 1], [0, -1], [-1, 0], [1, 0]]:
            moves, attacks = self.check_diagonal(direction, chessboard)
            if moves:
                available_moves += moves
            if attacks:
                available_attacks += attacks

        return available_moves, available_attacks

    def __str__(self):
        return 'R' if self.color == 'W' else 'r'


class King(Piece):
    def is_check(self, chessboard):
        current_position = np.array(self.get_position())
        all_attacks = []
        for direction in [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]]:
            _, attacks = self.check_diagonal(direction, chessboard)
            all_attacks += attacks
        
        if all_attacks:
            for position in all_attacks:
                piece = chessboard[position]
                _, piece_attacks = piece.get_moves(chessboard)
                if self.get_position() in piece_attacks:
                    return True

        for next_position in [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]:
            move = tuple(current_position + next_position)
            if self.check_move(move):
                piece = chessboard[move]
                if str(piece) in ['h', 'H'] and piece.color != self.color:
                    return True

        return False

    def get_moves(self, chessboard):
        available_moves = []
        available_attacks = []
        current_position = np.array([self.x, self.y])

        for direction in [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]]:
            next_position = current_position + direction

            if self.check_move(tuple(next_position)):
                if chessboard[tuple(next_position)] == None:
                    available_moves.append(tuple(next_position))

                elif isinstance(chessboard[tuple(next_position)], Piece) and chessboard[tuple(next_position)].color != self.color:
                    available_attacks.append(tuple(next_position))

        return available_moves, available_attacks

    def __str__(self):
        return 'K' if self.color == 'W' else 'k'


class Queen(Piece):
    def get_moves(self, chessboard):
        available_moves = []
        available_attacks = []

        for direction in [[0, 1], [0, -1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]]:
            moves, attacks = self.check_diagonal(direction, chessboard)
            if moves:
                available_moves += moves
            if attacks:
                available_attacks += attacks

        return available_moves, available_attacks

    def __str__(self):
        return 'Q' if self.color == 'W' else 'q'

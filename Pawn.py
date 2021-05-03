import numpy as np

# string przy kolorze
# BS BQ WS WQ  black b Black B 
class ChessEntity:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.start = True
    
    def move(self, move):
        for x in move:
            if x not in range(0, 7):
                raise ValueError('x should be between 0 and 7')
        
        self.x, self.y = move

# dekorator property (metody jako atrybuty)
# popraw metodę, uwzględnij ruchy czarnego piona (property nie przejdzie, )
# Google excel do notowania ile czasu upłynęło
class Pawn(ChessEntity):
    def available_moves(self, chessboard):
        available_moves = []
        available_attacks = []
        if chessboard[self.x, self.y+1] is None:
            available_moves.append((self.x, self.y+1))
            if self.start and chessboard[self.x, self.y+2] is None: 
                available_moves.append((self.x, self.y+2))

        attack_fields = (chessboard[self.x + 1, self.y + 1], chessboard[self.x - 1, self.y + 1])
        for attack_field in attack_fields:
            if attack_field is not None and attack_field.color != self.color:
                available_attacks.append((attack_field.x, attack_field.y))
        
        return available_moves, available_attacks

# logikę dać do chessboard, nie powinien zmieniać pól innej klasy
    def move(self, move, chessboard):
        x, y = move
        chessboard[x, y] = self
        chessboard[self.x, self.y] = None
        super().move(move)


    def __str__(self):
        return 'P'

import asyncio
import random
import json

from game_logic.chessboard import ChessBoard, ChessError
from player import Player

# Wrzuć to do env-ów
# Tego typu argumenty lepiej przesyłać do funkcji
# HEADER = 64
# PORT = 5050
# HOST = socket.gethostbyname(socket.gethostname())
# ADDR = (HOST, PORT)
# FORMAT = 'utf-8'
# AWAITING = '!AWAITING'
# TURN = '!TURN'
# DISCONNECT_MESSAGE = '!DISCONNECT'

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)


# player_move = {
#     'type': 'move',
#     'piece': [3, 1],
#     'move': [3, 3],
#     'color': 'W/B',
#     'isCheck': False # True
# }

# Stwórz singletona z klasy Server!!!

class Server:
    header = 64
    game_queue = []

    def __init__(self, address, port, str_format='utf-8'):
        self.address = address
        self.port = port
        self.format = str_format

    async def handle_game(self, player1, player2):
        '''
        1. Pobierz pion i ruch od gracza
        2. sprawdź czy ruch poprawny
        3. rusz się nim na szachownicy
        4. sprawdźczy któryś z graczy wygrał
        6. prześlij info o ruchu kolejnemu graczowi
        7. goto 1.
        '''
        game = ChessBoard()
        moving, awaiting = (player1, player2) if player1.color == 'W' else (
            player2, player1)
        await moving.send({
            'type': 'game_start',
            'assigned_color': moving.color,
            'enemy_player': awaiting.name
        })
        await awaiting.send({
            'type': 'game_start',
            'assigned_color': awaiting.color,
            'enemy_player': moving.name
        })
        playing = True
        while playing:
            move = await moving.receive()
            try:
                if move['type'] == 'chess-move':
                    game_piece, game_move = (move['piece'], move['move'])
                    game.move_piece(game_piece, game_move)
                    game_status = game.get_game_status()
                    game.print_board()
                    await moving.send({
                        'type': 'success',
                        'status': game_status,
                        'board': game.get_board()
                    })
                    await awaiting.send({
                        'type': 'move',
                        'move': move
                    })
                # wrzuć playerów do dicta i zmieniaj klucze
                moving, awaiting = (awaiting, moving)
            except ChessError as chess_error:
                print(chess_error)
                await moving.send({
                    'type': 'chess error',
                    'message': str(chess_error)
                })


# cors -> do bezpiecznego dzielenia się zasobami
# endpoint -> permission robisz socket server i wrzucasz w payload
# Self signed certificate

    async def handle_player(self, reader, writer):
        message = await reader.read(200)
        message = message.decode(self.format)
        player_data = json.loads(message)

        if 'name' not in player_data.keys():
            raise KeyError('Wrong connect message from player')

        writer.write(json.dumps({
            'type': 'search_game',
            'status': 'success',
            'message': 'searching for player'
        }).encode(self.format))
        await writer.drain()

        player = Player(
            player_data['name'],
            reader,
            writer
        )
# Global interpreter lock (GIL) w Pythonie
        queue_lock = asyncio.Lock()
        async with queue_lock:
            self.game_queue.append(player)

            if len(self.game_queue) >= 2:
                player_color = random.choice(['W', 'B'])
                player1 = self.game_queue.pop()
                player1.assign_color(player_color)
                player2 = self.game_queue.pop()
                player2.assign_color('W' if player_color == 'B' else 'B')
                asyncio.create_task(self.handle_game(player1, player2))

    async def start(self):
        server = await asyncio.start_server(self.handle_player, self.address, self.port)
        assigned_address = server.sockets[0].getsockname()
        print(
            f'[ RUNNING ] Server is running on {assigned_address}:{self.port}')

        async with server:
            await server.serve_forever()


def main():
    server = Server('127.0.0.1', 5050)
    asyncio.run(server.start())


main()
# dobrze dać header z długością wiadomości jako pierwsza wiadomość

# tab nine -> dodatek do pythona, kite


#
# Front -> Django
#
#
# Front (gry) -> server socket

import asyncio
import random
import string
import json

from player import Player

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = '127.0.1.1'
ADDR = (SERVER, PORT)

'''
connect = {
    'type': 'find_game',
    'color': 'W', # 'B' / 'R'
    'name': 'Player_name'
}
connect_response = {
    'type': 'find_game',
    'status': 'searching',
    'assigned_color': 'W', # 'B' / 'R'
}

game_start_response = {
    'type': 'game_start',
    'enemy_player': 'player_name',
    'turn': 'W'
}

player_move = {
    'type': 'move',
    'moveType': 'move/attack/acstling'.
    'piece': [3, 1],
    'move': [3, 3],
    'color': 'W/B',
    'isCheck': False # True
}

player_move_response = {
    'type: 'move'
    'status': 'success/error'
    'message': 'Illegal move (when error)'
}

enemy_move_response = {
    'type': 'enemy_move',
    'piece': [3, 1],
    'move': [3, 3],
    'moveType': 'move/attack/castling',
    'color': 'B/W',
    'isCheck': False, # True
    'endGame': False # True
}
'''

# lepiej w funkcji wszystko zamknąć niż globalnie -> wydajniej


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 5050)
    
    player_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    player = Player(player_name, reader, writer)
    writer.write(json.dumps({
        'type': 'join',
        'name': player_name
    }).encode(player.str_format))
    await writer.drain()

    message = await reader.read(200)
    message = message.decode(player.str_format)
    message = json.loads(message)

    if message['type'] == 'search_game':
        print('Searching for opponent')
        message = await player.receive()
        if message['type'] == 'game_start':
            playing = True
            turn = 'W'
            player.assign_color(message['assigned_color'])
            print(f'Color: {player.color}')
            while playing:
                if player.color == turn:
                    awaiting_move = True
                    while awaiting_move:
                        move = input('Give piece and move')
                        piece, move = move.split()
                        await player.send({
                            'type': 'chess-move',
                            'piece': piece,
                            'move': move
                        })
                        response = await player.receive()
                        print(response)
                else:
                    move = await player.receive()
                    print(f'Enemy move: {move}')
                turn = 'W' if turn == 'B' else 'B'

                

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client())
# board = ChessBoard()
# board.print_board()

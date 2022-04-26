import asyncio
import os
from queue import Queue
from dotenv import load_dotenv

from game_logic.chessboard import ChessBoard, ChessError
from utils.player import Player, SocketHandler


class Server:
    """Main class for chess server"""

    header = 64
    __player_queue = Queue()
    __players_connected = 0

    def __init__(self, address, port, str_format="utf-8"):
        self.address = address
        self.port = port
        self.format = str_format

    async def _handle_game(self, player1, player2):
        """
        1. Pobierz pion i ruch od gracza
        2. sprawdź czy ruch poprawny
        3. rusz się nim na szachownicy
        4. sprawdźczy któryś z graczy wygrał
        6. prześlij info o ruchu kolejnemu graczowi
        7. goto 1.
        """
        game = ChessBoard()
        players = {"p1": player1, "p2": player2}
        player_turn = "p1" if player1.color == "W" else "p2"
        for player in players.values():
            await player.send(
                {
                    "type": "game_start",
                    "assigned_color": player.color,
                    "enemy_player": player.name,
                }
            )

        playing = True
        while playing:
            move = await players[player_turn].receive()
            print(move)
            try:
                if move["type"] == "chess-move":
                    game_piece, game_move = (move["piece"], move["move"])
                    game.move_piece(game_piece, game_move)
                    game_status = game.get_game_status()
                    game.print_board()
                    await players[player_turn].send(
                        {
                            "type": "success",
                            "status": game_status,
                            "board": game.get_board(),
                        }
                    )
                    await players["p1" if player_turn == "p2" else "p2"].send(
                        {"type": "move", "move": move}
                    )
                player_turn = "p1" if player_turn == "p2" else "p2"

            except ChessError as chess_error:
                print(chess_error)
                await players[player_turn].send(
                    {"type": "chess error", "message": str(chess_error)}
                )

    # cors -> do bezpiecznego dzielenia się zasobami
    # endpoint -> permission robisz socket server i wrzucasz w payload
    # Self signed certificate

    async def _handle_player(self, reader, writer):
        socket_handler = SocketHandler(reader, writer)
        player_data = await socket_handler.receive()

        if "name" not in player_data.keys():
            raise KeyError("Wrong connect message from player")

        await socket_handler.send(
            {
                "type": "search_game",
                "status": "success",
                "message": "searching for player",
            }
        )

        player = Player(player_data["name"], socket_handler)
        print(f"[ PLAYER CONNECTED ] Player with name {player_data['name']} connected.")
        queue_lock = asyncio.Lock()
        async with queue_lock:
            self.__player_queue.put(player)

            if self.__player_queue.qsize() >= 2:
                player1 = self.__player_queue.get()
                player1.assign_color("W")

                player2 = self.__player_queue.get()
                player2.assign_color("B")

                asyncio.create_task(self._handle_game(player1, player2))

    async def start(self):
        """Starts chess server and listens for incoming client connections"""
        server = await asyncio.start_server(
            self._handle_player, self.address, self.port
        )
        assigned_address = server.sockets[0].getsockname()
        print(f"[ RUNNING ] Server is running on {assigned_address}:{self.port}")

        async with server:
            await server.serve_forever()


def main():
    """Main function to start server"""
    load_dotenv()
    hostname = os.environ.get("HOST_NAME")
    port = os.environ.get("PORT_NUMBER")
    server = Server(hostname, port)
    asyncio.run(server.start())


main()

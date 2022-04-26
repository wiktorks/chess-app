import json


class SocketHandler:
    """Class for handling socket communiaction

    Raises:
        IOError: _description_

    Returns:
        _type_: _description_
    """

    header_size = 64

    def __init__(self, reader, writer, str_format="utf-8"):
        self.reader = reader
        self.writer = writer
        self.str_format = str_format

    def _validate_header(self, header):
        if "!HEADER" not in header.keys():
            raise IOError("Message does not contain header")

        return header

    async def _write_to_buffer(self, msg):
        self.writer.write(msg)
        await self.writer.drain()

    async def receive(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        msg = await self.reader.read(self.header_size)
        msg = self._validate_header(json.loads(msg.decode(self.str_format)))

        msg_length = msg["!HEADER"]
        msg = await self.reader.read(msg_length)
        msg = json.loads(msg.decode(self.str_format))
        return msg

    async def send(self, message):
        """_summary_

        Args:
            message (_type_): _description_
        """
        msg = json.dumps(message)
        msg = msg.encode(self.str_format)
        header = json.dumps({"!HEADER": len(msg)})
        header = f'{" " * (self.header_size - len(header))}{header}'.encode(
            self.str_format
        )

        await self._write_to_buffer(header)
        await self._write_to_buffer(msg)


class Player:
    """
    Class for representing connected player
    """

    header_size = 64
    color = None

    def __init__(self, name, socket_handler: SocketHandler):
        self.name = name
        self.socket_handler = socket_handler

    def assign_color(self, color):
        """Assigns chess color to the player

        Args:
            color (str): White ("W") or Black ("B")

        Raises:
            ValueError: Color can only be "B" or "W"
        """
        if color not in ["W", "B"]:
            raise ValueError('Color can only be "B" or "W"')

        self.color = color

    async def send(self, message):
        """_summary_

        Args:
            message (_type_): _description_
        """
        await self.socket_handler.send(message)

    async def receive(self):
        """_summary_

        Args:
            message (_type_): _description_

        Returns:
            _type_: _description_
        """
        return_msg = await self.socket_handler.receive()
        return return_msg


# UUID4
# Komunikacja z serwerem Django (REST API)
# API do serwera z komunikacją do bazy danych (nowa aplikacja w Django)

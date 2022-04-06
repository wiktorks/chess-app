import json


class Player:
    header_size = 64
    color = None

    def __init__(self, name, reader, writer, str_format="utf-8"):
        self.name = name
        self.reader = reader
        self.writer = writer
        self.str_format = str_format

    def assign_color(self, color):
        self.color = color

    def _validate_header(self, header):
        if "!HEADER" not in header.keys():
            raise IOError("Message not containing header")

        return header

    async def _write_to_buffer(self, msg):
        self.writer.write(msg)
        await self.writer.drain()

    async def receive(self, validator):
        msg = await self.reader.read(self.header_size)
        msg = self._validate_header(json.loads(msg.decode(self.str_format)))

        msg_length = msg["!HEADER"]
        msg = await self.reader.read(msg_length)
        msg = json.loads(msg.decode(self.str_format))
        return validator(**msg)

    async def send(self, message):
        msg = json.dumps(message)
        msg = msg.encode(self.str_format)
        header = json.dumps({"!HEADER": len(msg)})
        header = f'{" " * (self.header_size - len(header))}{header}'.encode(
            self.str_format
        )

        await self._write_to_buffer(header)
        await self._write_to_buffer(msg)


# UUID4
# Komunikacja z serwerem Django (REST API)
# API do serwera z komunikacją do bazy danych (nowa aplikacja w Django)

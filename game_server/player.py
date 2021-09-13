import json

class Player():
    header_size = 64
    color = None

    def __init__(self, name, reader, writer, str_format='utf-8'):
        self.name = name
        self.reader = reader
        self.writer = writer
        self.str_format = str_format

    def assign_color(self, color):
        self.color = color

    async def _write_to_buffer(self, msg):
        self.writer.write(msg)
        await self.writer.drain()

    async def receive(self):
        msg = await self.reader.read(self.header_size)
        msg = json.loads(msg.decode(self.str_format))
        if '!HEADER' not in msg.keys():
            raise IOError('Message not containing header')

        msg_length = msg['!HEADER']
        msg = await self.reader.read(msg_length)
        msg = json.loads(msg.decode(self.str_format))
        return msg

    async def send(self, message):
        msg = json.dumps(message)
        msg = msg.encode(self.str_format)
        header = json.dumps({
            '!HEADER': len(msg)
        })
        header = f'{" " * (self.header_size - len(header))}{header}'.encode(self.str_format)

        await self._write_to_buffer(header)
        await self._write_to_buffer(msg)


# UUID4
# Komunikacja z serwerem Django (REST API)
# API do serwera z komunikacją do bazy danych (nowa aplikacja w Django)

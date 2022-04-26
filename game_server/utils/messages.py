from jsonschema import validate


class Message:
    """Base class for chess socket game messages"""

    def dict(self):
        """Get dict representation of the message object"""
        return self.__dict__


class ChessMoveMessage(Message):
    request_schema = {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "piece": {"type": "string", "pattern": "^[A-H][1-8]$"},
            "position": {"type": "string", "pattern": "^[A-H][1-8]$"},
        },
    }
    response_schema = {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "game_info": {"type": "string", "pattern": "^[A-H][1-8]$"},
            "board": {"type": "array"},
        },
    }

    def __init__(self, message: dict):
        super().__init__()

"""Custom exception classes"""


class ChessError(Exception):
    """_Base exception class for chess errors"""

    # pass


class ClientInputError(Exception):
    """Base exception class for socket client input"""

    def __init__(self, socket_message_type, error_message):
        super().__init__(error_message)

        self.sockert_message_type = socket_message_type
        self.error_message = error_message

class ClientInputError(Exception):
    def __init__(self, socket_message_type, error_message):
        self.sockert_message_type = socket_message_type
        self.error_message = error_message


def validate_join(**kwargs):
    if kwargs.get("type") != "join" or not isinstance(kwargs.get("name"), str):
        raise ClientInputError("join", "Wrong message type")

    return kwargs


def validate_move(**kwargs):
    if (
        not kwargs.get("piece")
        or not isinstance(kwargs.get("piece"), str)
        or len(kwargs.get("piece")) != 2
        or not kwargs.get("move")
        or not isinstance(kwargs.get("move"), str)
        or len(kwargs.get("move")) != 2
    ):
        raise ClientInputError("move", f"Wrong move message provided: {kwargs}")

    return kwargs

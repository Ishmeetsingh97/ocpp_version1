from enum import Enum


class MessageType(Enum):
    Call = 2
    CallResult = 3
    CallError = 4

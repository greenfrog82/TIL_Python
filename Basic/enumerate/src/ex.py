from enum import Enum, IntEnum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Shape(IntEnum):
    CIRCLE = 1
    SQUARE = 2

class Request(IntEnum):
    POST = 1
    GET = 2
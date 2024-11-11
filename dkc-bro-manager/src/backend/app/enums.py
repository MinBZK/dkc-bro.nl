from enum import Enum


class Importance(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3


class RuleType(Enum):
    SINGLE = 1
    GROUPED = 2

from enum import Enum


class ExType(str, Enum):
    BODYWEIGHT = "bodyweight"
    WEIGHTS = "weights"

class PRType(str, Enum):
    ONE_RM = "1rm"
    TWO_RM = "2rm"
    FIVE_RM = "5rm"
    AMRAP = "amrap"
    BODYWEIGHT = "bodyweight"
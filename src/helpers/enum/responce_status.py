from enum import Enum 

class ResponceStatus(str, Enum):
    LIKE = 'L'
    DISLIKE = 'D'
    NONE = 'N'
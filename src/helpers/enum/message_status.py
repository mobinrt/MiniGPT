from enum import Enum 

class MessageStatus(str, Enum):
    SENT = 'S'
    DELIVERED = 'D'
    READ = 'R'
    FAILED = 'F'
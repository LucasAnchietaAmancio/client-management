from enum import Enum

class ClientPriorityEnum(str, Enum):
    HIGH = "prioridade_alta"
    NORMAL = "prioridade_normal"
    NOT_PROCESSING = None

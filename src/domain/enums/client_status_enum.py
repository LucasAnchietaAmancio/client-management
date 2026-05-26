from enum import Enum

class ClientStatusEnum(str, Enum):
    WAITING_ANALYSIS = "Aguardando Análise"
    PROCESSED = "Processado"

import uuid

from src.domain.value_objects.name_value_object import NameValueObject
from src.domain.value_objects.email_value_object import EmailValueObject
from src.domain.value_objects.asset_value_object import AssetValueObject
from src.domain.value_objects.type_request_value_object import TypeRequestValueObject
from src.domain.enums.client_status_enum import ClientStatusEnum
from src.domain.enums.client_priority_enum import ClientPriorityEnum
class ClientEntity:
    def __init__(self,client_id: uuid.UUID,client_name: NameValueObject,client_email: EmailValueObject,type_request: TypeRequestValueObject,asset_value: AssetValueObject,status: ClientStatusEnum,priority: ClientPriorityEnum):
        self.client_id = client_id
        self.client_name = client_name
        self.client_email = client_email
        self.type_request = type_request
        self.asset_value = asset_value
        self.status = status
        self.priority = priority

    @staticmethod
    def create(client_name: str, client_email: str,type_request: str,asset_value: int) -> "ClientEntity":
        return ClientEntity(
            client_id=uuid.uuid4(),
            client_name=NameValueObject(client_name),
            client_email=EmailValueObject(client_email),
            type_request=TypeRequestValueObject(type_request),
            asset_value=AssetValueObject(asset_value),
            status=ClientStatusEnum.WAITING_ANALYSIS,
            priority=ClientPriorityEnum.NOT_PROCESSING,
        )

    @staticmethod
    def restore(client_id: str | uuid.UUID, client_name: str,client_email: str,type_request: str,asset_value: int,status: str | ClientStatusEnum,priority: str | ClientPriorityEnum,) -> "ClientEntity":
        return ClientEntity(
            client_id=uuid.UUID(str(client_id)),
            client_name=NameValueObject(client_name),
            client_email=EmailValueObject(client_email),
            type_request=TypeRequestValueObject(type_request),
            asset_value=AssetValueObject(asset_value),
            status=ClientStatusEnum(status),
            priority=ClientPriorityEnum(priority),
        )

    def process(self) -> None:
        self.status = ClientStatusEnum.PROCESSED
        self.priority = self._calculate_priority()

    def _calculate_priority(self) -> ClientPriorityEnum:
        if self.asset_value.value >= 200000:
            return ClientPriorityEnum.HIGH

        return ClientPriorityEnum.NORMAL

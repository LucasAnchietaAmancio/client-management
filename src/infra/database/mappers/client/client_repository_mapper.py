from src.domain.entities.client_entity import ClientEntity

class ClientRepositoryMapper:

    @staticmethod
    def to_domain(record: object) -> ClientEntity:
        return ClientEntity.restore(
            client_id=record.client_id,
            client_name=record.client_name,
            client_email=record.client_email,
            type_request=record.type_request,
            asset_value=record.asset_value,
            status=record.status,
            priority=record.priority,
        )

    @staticmethod
    def to_persistence(client_entity: ClientEntity) -> dict:
        return {
            "client_id": str(client_entity.client_id),
            "client_name": client_entity.client_name.value,
            "client_email": client_entity.client_email.value,
            "type_request": client_entity.type_request.value,
            "asset_value": client_entity.asset_value.value,
            "status": client_entity.status.value,
            "priority": client_entity.priority.value,
        }

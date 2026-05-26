from domain.entities.client_entity import ClientEntity


class ClientRepositoryMapper:

    @staticmethod
    def to_domain(record: object) -> ClientEntity:
        return ClientEntity.restore(
            client_id=record.client_id,
            name=record.name,
            email=record.email,
            type_request=record.type_request,
            asset_value=record.asset_value,
            status=record.status,
            priority=record.priority,
        )

    @staticmethod
    def to_public(record: object) -> object:
        return {
            "client_id": record.client_id,
            "name": record.name,
            "email": record.email,
            "type_request": record.type_request,
            "asset_value": record.asset_value,
        }

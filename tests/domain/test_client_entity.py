import unittest

from domain.entities.client_entity import ClientEntity
from domain.enums.client_priority_enum import ClientPriorityEnum
from domain.enums.client_status_enum import ClientStatusEnum


class TestClientEntity(unittest.TestCase):
    def test_create_client_with_initial_status(self):
        client = ClientEntity.create(
            name="Lucas",
            email="LUCAS@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
        )

        self.assertEqual(client.name.value,"Lucas")
        self.assertEqual(client.email.value,"lucas@email.com")
        self.assertEqual(client.type_request.value,"Atualizacao cadastral")
        self.assertEqual(client.status,ClientStatusEnum.WAITING_ANALYSIS)
        self.assertEqual(client.priority,ClientPriorityEnum.NOT_PROCESSING)

    def test_process_client_with_high_priority(self):
        client = ClientEntity.create(
            name="Lucas",
            email="lucas@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
        )

        client.process()

        self.assertEqual(client.status,ClientStatusEnum.PROCESSED)
        self.assertEqual(client.priority,ClientPriorityEnum.HIGH)

    def test_process_client_with_normal_priority(self):
        client = ClientEntity.create(
            name="Maria Souza",
            email="maria.souza@example.com",
            type_request="Atualizacao cadastral",
            asset_value=150000,
        )

        client.process()

        self.assertEqual(client.status,ClientStatusEnum.PROCESSED)
        self.assertEqual(client.priority,ClientPriorityEnum.NORMAL)

    def test_restore_client_from_database_values(self):
        client = ClientEntity.restore(
            client_id="11111111-1111-1111-1111-111111111111",
            name="Lucas",
            email="lucas@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
            status="Processado",
            priority="prioridade_alta",
        )

        self.assertEqual(client.status,ClientStatusEnum.PROCESSED)
        self.assertEqual(client.priority,ClientPriorityEnum.HIGH)


if __name__ == "__main__":
    unittest.main()

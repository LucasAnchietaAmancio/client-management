import unittest
from types import SimpleNamespace

from src.domain.entities.client_entity import ClientEntity
from src.infra.exceptions.fail_persist_on_database import FailPersistOnDatabase
from src.infra.exceptions.fail_search_on_database import FailSearchOnDatabase
from src.infra.exceptions.fail_update_on_database import FailUpdateOnDatabase
from src.infra.database.repositories.client.client_repository import ClientRepository


class FakeClientDelegate:
    def __init__(self) -> None:
        self.records: list[dict] = []
        self.should_fail_on_create = False
        self.should_fail_on_find = False
        self.should_fail_on_update = False

    async def create(self,data: dict) -> object:
        if self.should_fail_on_create:
            raise RuntimeError("database unavailable")

        self.records.append(data)
        return SimpleNamespace(**data)

    async def find_unique(self,where: dict) -> object | None:
        if self.should_fail_on_find:
            raise RuntimeError("database unavailable")

        client_email = where["client_email"]

        for record in self.records:
            if record["client_email"] == client_email:
                return SimpleNamespace(**record)

        return None

    async def update(self,where: dict,data: dict) -> object:
        if self.should_fail_on_update:
            raise RuntimeError("database unavailable")

        client_id = where["client_id"]

        for record in self.records:
            if record["client_id"] == client_id:
                record.update(data)
                return SimpleNamespace(**record)

        raise RuntimeError("use_cases not found")


class PrismaClient:
    def __init__(self) -> None:
        self.client = FakeClientDelegate()


class TestClientRepository(unittest.IsolatedAsyncioTestCase):
    async def test_save_persists_client_and_returns_none(self):
        db = PrismaClient()
        repository = ClientRepository(db)
        client = ClientEntity.create(
            client_name="Lucas",
            client_email="lucas@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
        )

        saved_client = await repository.save(client)

        self.assertEqual(len(db.client.records),1)
        self.assertEqual(db.client.records[0]["client_email"],"lucas@email.com")
        self.assertEqual(db.client.records[0]["asset_value"],250000)
        self.assertIsNone(saved_client)

    async def test_find_by_client_email_returns_restored_client(self):
        db = PrismaClient()
        repository = ClientRepository(db)
        client = ClientEntity.create(
            client_name="Lucas",
            client_email="lucas@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
        )

        await repository.save(client)
        found_client = await repository.find_by_client_email("lucas@email.com")

        self.assertIsNotNone(found_client)
        self.assertEqual(found_client.client_email.value,"lucas@email.com")

    async def test_find_by_client_email_returns_none_when_client_does_not_exist(self):
        db = PrismaClient()
        repository = ClientRepository(db)

        found_client = await repository.find_by_client_email("missing@example.com")

        self.assertIsNone(found_client)

    async def test_update_by_id_updates_client_and_returns_none(self):
        db = PrismaClient()
        repository = ClientRepository(db)
        client = ClientEntity.create(
            client_name="Lucas",
            client_email="lucas@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
        )

        await repository.save(client)
        client.process()
        updated_client = await repository.update_by_id(client)

        self.assertIsNone(updated_client)
        self.assertEqual(db.client.records[0]["status"],"Processado")
        self.assertEqual(db.client.records[0]["priority"],"prioridade_alta")

    async def test_save_raises_infra_exception_when_database_fails(self):
        db = PrismaClient()
        db.client.should_fail_on_create = True
        repository = ClientRepository(db)
        client = ClientEntity.create(
            client_name="Lucas",
            client_email="lucas@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
        )

        with self.assertRaises(FailPersistOnDatabase):
            await repository.save(client)

    async def test_find_by_client_email_raises_infra_exception_when_database_fails(self):
        db = PrismaClient()
        db.client.should_fail_on_find = True
        repository = ClientRepository(db)

        with self.assertRaises(FailSearchOnDatabase):
            await repository.find_by_client_email("lucas@email.com")

    async def test_update_by_id_raises_infra_exception_when_database_fails(self):
        db = PrismaClient()
        db.client.should_fail_on_update = True
        repository = ClientRepository(db)
        client = ClientEntity.create(
            client_name="Lucas",
            client_email="lucas@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
        )

        with self.assertRaises(FailUpdateOnDatabase):
            await repository.update_by_id(client)


if __name__ == "__main__":
    unittest.main()

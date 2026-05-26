import unittest
from types import SimpleNamespace

from domain.entities.client_entity import ClientEntity
from infra.exceptions.fail_persist_on_database import FailPersistOnDatabase
from infra.exceptions.fail_search_on_database import FailSearchOnDatabase
from infra.repositories.client_repository import ClientRepository


class FakeClientDelegate:
    def __init__(self) -> None:
        self.records: list[dict] = []
        self.should_fail_on_create = False
        self.should_fail_on_find = False

    async def create(self,data: dict) -> object:
        if self.should_fail_on_create:
            raise RuntimeError("database unavailable")

        self.records.append(data)
        return SimpleNamespace(**data)

    async def find_unique(self,where: dict) -> object | None:
        if self.should_fail_on_find:
            raise RuntimeError("database unavailable")

        email = where["email"]

        for record in self.records:
            if record["email"] == email:
                return SimpleNamespace(**record)

        return None


class FakePrismaDatabase:
    def __init__(self) -> None:
        self.client = FakeClientDelegate()


class TestClientRepository(unittest.IsolatedAsyncioTestCase):
    async def test_save_persists_client_and_returns_public_object(self):
        db = FakePrismaDatabase()
        repository = ClientRepository(db)
        client = ClientEntity.create(
            name="Lucas",
            email="lucas@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
        )

        saved_client = await repository.save(client)

        self.assertEqual(len(db.client.records),1)
        self.assertEqual(db.client.records[0]["email"],"lucas@email.com")
        self.assertEqual(db.client.records[0]["asset_value"],250000)
        self.assertEqual(saved_client["client_id"],str(client.client_id))
        self.assertEqual(saved_client["name"],"Lucas")
        self.assertEqual(saved_client["email"],"lucas@email.com")
        self.assertEqual(saved_client["type_request"],"Atualizacao cadastral")
        self.assertEqual(saved_client["asset_value"],250000)

    async def test_find_by_email_returns_restored_client(self):
        db = FakePrismaDatabase()
        repository = ClientRepository(db)
        client = ClientEntity.create(
            name="Lucas",
            email="lucas@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
        )

        await repository.save(client)
        found_client = await repository.find_by_email("lucas@email.com")

        self.assertIsNotNone(found_client)
        self.assertEqual(found_client.email.value,"lucas@email.com")

    async def test_find_by_email_returns_none_when_client_does_not_exist(self):
        db = FakePrismaDatabase()
        repository = ClientRepository(db)

        found_client = await repository.find_by_email("missing@example.com")

        self.assertIsNone(found_client)

    async def test_save_raises_infra_exception_when_database_fails(self):
        db = FakePrismaDatabase()
        db.client.should_fail_on_create = True
        repository = ClientRepository(db)
        client = ClientEntity.create(
            name="Lucas",
            email="lucas@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
        )

        with self.assertRaises(FailPersistOnDatabase):
            await repository.save(client)

    async def test_find_by_email_raises_infra_exception_when_database_fails(self):
        db = FakePrismaDatabase()
        db.client.should_fail_on_find = True
        repository = ClientRepository(db)

        with self.assertRaises(FailSearchOnDatabase):
            await repository.find_by_email("lucas@email.com")


if __name__ == "__main__":
    unittest.main()

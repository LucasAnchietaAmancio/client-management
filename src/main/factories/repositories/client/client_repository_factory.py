from src.infra.database.repositories.client.client_repository import ClientRepository
from src.main.factories.database.prisma_client_factory import make_prisma_client

def make_client_repository() -> ClientRepository:
    db = make_prisma_client().get_client()
    return ClientRepository(db)

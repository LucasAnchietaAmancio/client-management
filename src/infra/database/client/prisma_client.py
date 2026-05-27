from typing import Any
from src.infra.exceptions.fail_database_connection import FailDatabaseConnection
class PrismaClient:
    def __init__(self, prisma_provider: Any) -> None:
        self.prisma_provider = prisma_provider
        self.db = None

    async def connect(self) -> Any:
        if self.db is None:
            self.db = self.prisma_provider()
            await self.db.connect()

        return self.db

    async def disconnect(self) -> None:
        if self.db is not None:
            await self.db.disconnect()
            self.db = None

    def get_client(self) -> Any:
        if self.db is None:
            raise FailDatabaseConnection("Prisma client is not connected")

        return self.db

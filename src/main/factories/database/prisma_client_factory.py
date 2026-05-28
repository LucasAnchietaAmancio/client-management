from prisma import Prisma

from src.infra.database.client.prisma_client import PrismaClient

prisma_client = PrismaClient(Prisma)

def make_prisma_client() -> PrismaClient:
    return prisma_client

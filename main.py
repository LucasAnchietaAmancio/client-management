from fastapi import APIRouter, Depends, FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.main.app import App
from src.main.factories.database.prisma_client_factory import make_prisma_client

app = App(
    app=FastAPI(title="Client Management API"),
    router=APIRouter(),
    depends=Depends,
    status=status,
    prisma_client=make_prisma_client(),
    json_response=JSONResponse,
    request_validation_error=RequestValidationError,
).setup()

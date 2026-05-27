from fastapi import APIRouter, Depends, FastAPI, status

from src.main.app import App

app = App(
    app=FastAPI(title="Client Management API"),
    router=APIRouter(),
    depends=Depends,
    status=status,
).setup()

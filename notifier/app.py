from fastapi import FastAPI

from api.routers import api_router

app = FastAPI(title='Notify service')

app.include_router(api_router)

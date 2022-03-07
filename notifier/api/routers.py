from fastapi import APIRouter

from .messages import messages
from .users import users

api_router = APIRouter()

api_router.include_router(messages.router, tags=['messages'])
api_router.include_router(users.router, tags=['users'])

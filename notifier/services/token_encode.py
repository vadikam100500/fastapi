import os

import jwt
from dotenv import load_dotenv

from db.schemas import FakeTokenPayload

load_dotenv()

ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')


async def get_user_id(token: str) -> str:
    """Get user_id by token."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return str(FakeTokenPayload(**payload).user_id)


def create_access_token(data: dict):
    """Encode user_id to token."""
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

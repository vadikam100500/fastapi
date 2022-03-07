from pydantic import BaseModel


class FakeTokenPayload(BaseModel):
    user_id: int

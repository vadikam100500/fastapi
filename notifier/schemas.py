# import datetime as dt

from pydantic import BaseModel


class FakeTokenPayload(BaseModel):
    user_id: int = None


class Registration(BaseModel):
    message: str


class Confirmation(Registration):
    # date: dt.datetime
    date: str

    class Config:
        schema_extra = {
            "example": {
                "message": "TEXT BODY",
                "date": "2022-02-28 13:03:08.435389",
            }
        }


class Invite(Confirmation):
    pass

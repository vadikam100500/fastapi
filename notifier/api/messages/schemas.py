# import datetime as dt

from pydantic import BaseModel


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


class Delay(Confirmation):
    client_id: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": "Some id",
                "message": "TEXT BODY",
                "date": "2022-02-28 13:03:08.435389",
            }
        }

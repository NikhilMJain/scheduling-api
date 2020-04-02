from datetime import datetime

from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class NoteDB(NoteSchema):
    id: int


class UserRegistration(BaseModel):
    username: str
    email: str
    token: str = None


class User(BaseModel):
    user_id: int
    username: str
    token: str
    email: str


class Datetime(object):
    pass


class Slot(BaseModel):
    slot_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    is_available: bool
    duration: int


class Meeting(BaseModel):
    meeting_id: int
    slot_id: int
    status: int

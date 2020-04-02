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


class Slot(BaseModel):
    slot_id: int
    user_id: int
    start_time: str
    end_time: str
    is_available: bool
    duration: int


class Meeting(BaseModel):
    meeting_id: int
    slot_id: int
    status: int

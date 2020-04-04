import datetime
from typing import List

from pydantic import BaseModel, conlist


class UserRegistration(BaseModel):
    email: str


class TimeRange(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime


class AvailableSlots(BaseModel):
    date: datetime.date
    time_intervals: List[TimeRange]


class UserResponse(BaseModel):
    user_id: int
    email: str


class User(UserResponse):
    token: str
    username: str


class Slot(BaseModel):
    slot_id: int
    user_id: int
    start_time: datetime.datetime
    is_available: bool


class Meeting(BaseModel):
    meeting_id: int
    slot_id: int
    status: int


class MeetingPayload(BaseModel):
    slot_id: int
    guest_email_ids: List[str]
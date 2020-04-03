import datetime
from typing import List

from pydantic import BaseModel


class UserRegistration(BaseModel):
    username: str
    email: str
    token: str = None


class TimeRange(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime


class AvailableSlots(BaseModel):
    date: datetime.date
    time_intervals: List[TimeRange]


class User(BaseModel):
    user_id: int
    username: str
    token: str
    email: str


class Slot(BaseModel):
    slot_id: int
    user_id: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    is_available: bool
    duration: int


class Meeting(BaseModel):
    meeting_id: int
    slot_id: int
    status: int

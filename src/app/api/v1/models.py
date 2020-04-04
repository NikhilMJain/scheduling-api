import datetime
from typing import List

from pydantic import BaseModel, conlist


class NewUser(BaseModel):
    email: str
    first_name: str
    last_name: str


class TimeRange(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime


class AvailableSlots(BaseModel):
    date: datetime.date
    time_intervals: conlist(TimeRange, min_items=1)


class UserResponse(BaseModel):
    user_id: int
    email: str
    first_name: str
    last_name: str


class User(UserResponse):
    token: str
    calendar_id: str = None


class Slot(BaseModel):
    slot_id: int
    user_id: int
    start_time: datetime.datetime
    is_available: bool


class Meeting(BaseModel):
    meeting_id: int
    slot_id: int
    status: str
    subject: str
    notes: str = None


class MeetingPayload(BaseModel):
    slot_id: int
    subject: str
    notes: str = None
    guest_email_ids: List[str] = list()



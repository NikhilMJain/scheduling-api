from enum import Enum


class MeetingStatus(Enum):
    Scheduled = 1
    Cancelled = 2


class MeetingType(str, Enum):
    created = 'created'
    scheduled = 'scheduled'
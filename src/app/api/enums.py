from enum import Enum


class MeetingStatus(Enum):
    Scheduled = 1
    Cancelled = 2


class MeetingMemberRole(Enum):
    Scheduler = 1
    Guest = 2
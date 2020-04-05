from datetime import timedelta, datetime
from typing import List

from databases.backends.postgres import Record
from fastapi import HTTPException

from src.app.api.base_crud import BaseCRUD
from src.app.api.v1.enums import MeetingStatus
from src.app.api.v1.models import MeetingPayload, User
from src.app.database import slots, meetings, meeting_guests, database
from src.integrations.google_calendar.create_calendar_event import GoogleCalendarHandler


class MeetingManager(object):

    @database.transaction()
    async def schedule_new_meeting(self, meeting: MeetingPayload, current_user: User) -> int:
        slot = await self._get_slot(meeting.slot_id)
        self._validate_slot(slot)
        meeting_id = await self._create_meeting(meeting, current_user)
        await self._add_guests_to_meeting(meeting_id, meeting.guest_email_ids)
        await self._mark_slot_status_as_unavailable(meeting.slot_id)
        if current_user.calendar_id:
            self._create_event_in_google_calendar(current_user, meeting, slot.get('start_time'))
        return meeting_id

    async def _get_slot(self, slot_id) -> Record:
        slot = await BaseCRUD().fetch(model=slots, where=(slots.c.slot_id == slot_id))
        return slot

    def _validate_slot(self, slot) -> None:
        if not slot:
            raise HTTPException(status_code=404, detail='Slot not found')
        if not slot.get('is_available'):
            raise HTTPException(status_code=424, detail='Slot not available')

    async def _create_meeting(self, meeting: MeetingPayload, current_user: User) -> int:
        return await BaseCRUD().insert(model=meetings, values=dict(slot_id=meeting.slot_id,
                                                                   creator_id=current_user.user_id,
                                                                   status=MeetingStatus.Scheduled.name,
                                                                   subject=meeting.subject, notes=meeting.notes))

    async def _add_guests_to_meeting(self, meeting_id: int, guest_emails: List[str]) -> List[int]:
        values = list()
        for email in guest_emails:
            values.append(dict(meeting_id=meeting_id, email=email))
        return await BaseCRUD().bulk_insert(model=meeting_guests, values=values)

    async def _mark_slot_status_as_unavailable(self, slot_id: int) -> None:
        await BaseCRUD().update(model=slots, where=(slot_id == slots.c.slot_id), values=dict(is_available=False))

    def _create_event_in_google_calendar(self, current_user: User, meeting: MeetingPayload,
                                         start_time: datetime) -> None:
        end_time = start_time + timedelta(hours=1)
        guest_email_ids = meeting.guest_email_ids + [current_user.email]
        GoogleCalendarHandler().create_event(calendar_id=current_user.calendar_id, start_time=start_time,
                                             end_time=end_time, subject=meeting.subject, notes=meeting.notes,
                                             guest_emails=guest_email_ids)

    async def get_created_meetings(self, current_user: User) -> List[Record]:
        return await BaseCRUD().fetch_all(model=meetings, where=(current_user.user_id == meetings.c.creator_id))

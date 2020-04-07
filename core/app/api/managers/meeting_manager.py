from datetime import timedelta, datetime
from typing import List, Dict

from databases.backends.postgres import Record
from fastapi import HTTPException

from core.app.api.base_crud import BaseCRUD
from core.app.api.v1 import config
from core.app.api.v1.enums import MeetingStatus
from core.app.api.v1.models import MeetingPayload, User
from core.app.database import slots, meetings, meeting_guests, database, users
from core.app.logger import log
from core.integrations.google_calendar.google_calendar_handler import GoogleCalendarHandler


class MeetingManager(object):

    @database.transaction()
    async def schedule_new_meeting(self, meeting: MeetingPayload, current_user: User) -> int:
        slot = await self._get_slot(meeting.slot_id)
        self._validate_slot(slot)
        meeting_id = await self._create_meeting(meeting=meeting, current_user=current_user)
        await self._add_guests_to_meeting(meeting_id=meeting_id, guest_emails=meeting.guest_email_ids)
        await self._mark_slot_status_as_unavailable(slot_id=meeting.slot_id)
        await self._create_event_in_google_calendar(user_id=slot.get('user_id'), meeting=meeting,
                                                    start_time=slot.get('start_time'), current_user=current_user)
        return meeting_id

    async def _get_slot(self, slot_id) -> dict:
        slot = await BaseCRUD().fetch(model=slots, where=(slots.c.slot_id == slot_id))
        return slot

    def _validate_slot(self, slot: dict) -> None:
        if not slot:
            raise HTTPException(status_code=404, detail='Slot not found')
        if not slot.get('is_available'):
            raise HTTPException(status_code=424, detail='Slot not available')

    async def _create_meeting(self, meeting: MeetingPayload, current_user: User) -> int:
        log.info('Inserting new meeting {}'.format(meeting))
        return await BaseCRUD().insert(model=meetings, values=dict(slot_id=meeting.slot_id,
                                                                   creator_id=current_user.user_id,
                                                                   status=MeetingStatus.Scheduled.name,
                                                                   subject=meeting.subject, notes=meeting.notes))

    async def _add_guests_to_meeting(self, meeting_id: int, guest_emails: List[str]) -> None:
        log.info('Adding guests to meeting_id {}'.format(meeting_id))
        values = list()
        for email in guest_emails:
            values.append(dict(meeting_id=meeting_id, email=email))
        return await BaseCRUD().bulk_insert(model=meeting_guests, values=values)

    async def _mark_slot_status_as_unavailable(self, slot_id: int) -> None:
        log.info('Mark slot as unavailable {}'.format(slot_id))
        await BaseCRUD().update(model=slots, where=(slot_id == slots.c.slot_id), values=dict(is_available=False))

    async def _create_event_in_google_calendar(self, user_id: int, meeting: MeetingPayload,
                                               start_time: datetime, current_user) -> None:
        try:
            user = await self._get_user(user_id)
            calendar_id = user.get('calendar_id')
            if not calendar_id:
                return
            log.info('Creating event in Google calendar ID {}'.format(calendar_id))
            end_time = start_time + timedelta(hours=1)
            guest_email_ids = meeting.guest_email_ids + [current_user.email, calendar_id]
            GoogleCalendarHandler().create_event(calendar_id=config.CALENDAR_ID, start_time=start_time,
                                                 end_time=end_time, subject=meeting.subject, notes=meeting.notes,
                                                 guest_emails=guest_email_ids)
        except Exception as e:
            log.error('Google Calendar failure {}'.format(e))

    async def get_created_meetings(self, current_user: User) -> List[Record]:
        log.info('Get created meetings for {}'.format(current_user.email))
        return await BaseCRUD().fetch_all(model=meetings, where=(current_user.user_id == meetings.c.creator_id))

    async def _get_user(self, user_id: int) -> Dict:
        return await BaseCRUD().fetch(model=users, where=(users.c.user_id == user_id))

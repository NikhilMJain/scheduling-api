from typing import List

from fastapi import Depends, APIRouter, HTTPException

from src.app.api.v1.auth import get_auth_user
from src.app.api.v1.enums import MeetingStatus, MeetingType
from src.app.api.v1.models import User, UserResponse, MeetingPayload
from src.app.database import slots, database, meetings, meeting_guests

router = APIRouter()


@router.post('/meetings/', status_code=201)
async def schedule_new_meeting(payload: MeetingPayload, current_user: User = Depends(get_auth_user)):
    slot = await database.fetch_one(slots.select().where(slots.c.slot_id == payload.slot_id))

    if not slot:
        raise HTTPException(status_code=404, detail='Slot not found')
    if not slot.get('is_available'):
        raise HTTPException(status_code=424, detail='Slot not available')

    meeting_id = await database.execute(
        meetings.insert().values(slot_id=payload.slot_id, creator_id=current_user.user_id,
                                 status=MeetingStatus.Scheduled.name))
    for email in payload.guest_email_ids:
        await database.execute(meeting_guests.insert().values(meeting_id=meeting_id, email=email))

    await database.execute(slots.update().where(payload.slot_id == slots.c.slot_id).values(is_available=False))

    return {'meeting_id': meeting_id}


@router.get('/meetings/', response_model=List[UserResponse])
async def get_meetings(type: MeetingType, current_user: User = Depends(get_auth_user)):
    if type == MeetingType.created:
        query = meetings.select().where(current_user.user_id == meetings.c.creator_id)
    else:
        query = 1 # query later
    all_users = await database.fetch_all(query)
    return all_users

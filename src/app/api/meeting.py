from datetime import timedelta
from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import and_

from src.app.api.auth import get_auth_user
from src.app.api.enums import MeetingStatus
from src.app.api.models import User, Slot, AvailableSlots, UserResponse, MeetingPayload, MeetingType
from src.app.database import slots, database, users, meetings, meeting_guests

router = APIRouter()


@router.get('/slots/', response_model=List[Slot])
async def get_available_slots(user_id: int, current_user: User = Depends(get_auth_user)):
    query = slots.select().where(and_(slots.c.user_id == user_id, slots.c.is_available == True))
    available_slots = await database.fetch_all(query)
    return available_slots


@router.post('/slots/', status_code=201)
async def specify_available_slots(payload: List[AvailableSlots], current_user: User = Depends(get_auth_user)):
    try:
        for item in payload:
            for interval in item.time_intervals:
                hours = (interval.end_time - interval.start_time).seconds // 3600
                for hour in range(hours):
                    start_time = interval.start_time + timedelta(hours=hour)
                    query = slots.insert().values(date=item.date, user_id=current_user.user_id, start_time=start_time,
                                                  is_available=True)
                    await database.execute(query)
    except Exception as e:
        # log here later
        pass
    return {}


@router.get('/users/', response_model=List[UserResponse])
async def get_all_users(current_user: User = Depends(get_auth_user)):
    query = users.select()
    all_users = await database.fetch_all(query)
    return all_users


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

from datetime import timedelta
from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy import and_

from src.app.api.auth import get_current_user
from src.app.api.models import User, Slot, AvailableSlots
from src.app.database import slots, database

router = APIRouter()


@router.get('/{user_id}/slots/', response_model=List[Slot])
async def get_slots(user_id: int, current_user: User = Depends(get_current_user)):
    query = slots.select().where(and_(slots.c.user_id == user_id, slots.c.is_available == True))
    available_slots = await database.fetch_all(query)
    return available_slots


@router.post('/slots/', status_code=201)
async def specify_available_slots(payload: List[AvailableSlots], current_user: User = Depends(get_current_user)):
    for item in payload:
        for interval in item.time_intervals:
            hours = (interval.end_time - interval.start_time).seconds // 3600
            for hour in range(hours):
                start_time = interval.start_time + timedelta(hours=hour)
                query = slots.insert().values(date=item.date, user_id=current_user.user_id, start_time=start_time,
                                              is_available=True)
                await database.execute(query)
    return {}
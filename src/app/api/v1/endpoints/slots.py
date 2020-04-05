from datetime import timedelta
from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy import and_

from src.app.api.v1.auth import get_auth_user
from src.app.api.v1.models import Slot, User, AvailableSlots
from src.app.database import slots, database

router = APIRouter()


@router.get('/v1/slots/', response_model=List[Slot], tags='slots')
async def get_available_slots(user_id: int, current_user: User = Depends(get_auth_user)):
    query = slots.select().where(and_(slots.c.user_id == user_id, slots.c.is_available == True))
    available_slots = await database.fetch_all(query)
    return available_slots


@router.post('/v1/slots/', status_code=201, tags='slots')
async def specify_available_slots(payload: List[AvailableSlots], current_user: User = Depends(get_auth_user)):
    try:
        values = list()
        query = slots.insert()
        for item in payload:
            for interval in item.time_intervals:
                hours = (interval.end_time - interval.start_time).seconds // 3600
                for hour in range(hours):
                    start_time = interval.start_time + timedelta(hours=hour)
                    values.append(dict(date=item.date, user_id=current_user.user_id, start_time=start_time,
                                       is_available=True))
        await database.execute_many(query=query, values=values)
    except Exception as e:
        # log here later
        pass
    return {}

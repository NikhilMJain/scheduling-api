from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy import and_

from src.app.api.auth import get_current_user
from src.app.api.models import User, Slot
from src.app.database import slots, database

router = APIRouter()


@router.get('/{user_id}/slots/', response_model=List[Slot])
async def get_slots(user_id: int, current_user: User = Depends(get_current_user)):
    query = slots.select().where(and_(slots.c.user_id == user_id, slots.c.is_available == True))
    available_slots = await database.fetch_all(query)
    return available_slots

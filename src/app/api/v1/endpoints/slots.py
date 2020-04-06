import datetime
from typing import List

from fastapi import Depends, APIRouter

from src.app.api.managers.slot_manager import SlotManager
from src.app.api.v1.auth import get_auth_user
from src.app.api.v1.models import Slot, User, AvailableSlots

router = APIRouter()


@router.get('/users/{user_id}/slots/', response_model=List[Slot])
async def get_available_slots(user_id: int, date: datetime.date = None, current_user: User = Depends(get_auth_user)):
    return await SlotManager().get_available_slots_for_user(user_id, date)


@router.post('/slots/', status_code=201)
async def define_available_slots(payload: List[AvailableSlots], current_user: User = Depends(get_auth_user)):
    await SlotManager().define_available_slots(available_slots=payload, current_user=current_user)
    return {}

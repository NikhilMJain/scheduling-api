from datetime import timedelta
from typing import List

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from sqlalchemy import and_

from src.app.api.base_crud import BaseCRUD
from src.app.api.v1.models import AvailableSlots, User
from src.app.database import slots, database
from src.app.logger import log


class SlotManager:
    async def get_available_slots_for_user(self, user_id):
        log.info('Get slots for user id {}'.format(user_id))
        return await BaseCRUD().fetch_all(model=slots, where=and_(slots.c.user_id == user_id, slots.c.is_available ==
                                                                  True))

    @database.transaction()
    async def define_available_slots(self, available_slots: List[AvailableSlots], current_user: User):
        log.info('Defining slots for {} - {}'.format(current_user.email, available_slots))
        try:
            values = self._get_all_values_to_insert(available_slots, current_user)
            return await self._insert_new_slots(values)
        except UniqueViolationError as e:
            log.error('Duplicate inserts - {}'.format(e))
            raise HTTPException(status_code=400, detail='Slot already exists for user')

    def _get_values_for_interval(self, slot, interval, current_user):
        values = list()
        hours = (interval.end_time - interval.start_time).seconds // 3600
        for hour in range(hours):
            start_time = interval.start_time + timedelta(hours=hour)
            values.append(dict(date=slot.date, user_id=current_user.user_id, start_time=start_time,
                               is_available=True))
        return values

    def _get_all_values_to_insert(self, available_slots, current_user):
        values = list()
        for slot in available_slots:
            for interval in slot.time_intervals:
                values.extend(self._get_values_for_interval(slot, interval, current_user))
        return values

    async def _insert_new_slots(self, values):
        return await BaseCRUD().bulk_insert(model=slots, values=values)

import secrets
from typing import Dict

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from psycopg2._psycopg import IntegrityError

from core.app.api.base_crud import BaseCRUD
from core.app.api.v1.models import NewUser
from core.app.database import users, database


class UserManager(object):
    async def get_user_by_id(self, user_id: int) -> Dict:
        return await BaseCRUD().fetch(model=users, where=(users.c.user_id == user_id))

    @database.transaction()
    async def add_user(self, user: NewUser) -> dict:
        try:
            token = secrets.token_hex(20)
            user_id = await self._insert_user(user, token)
        except (IntegrityError, UniqueViolationError):
            raise HTTPException(status_code=400, detail='Email address already exists')
        return dict(user_id=user_id, email=user.email, token=token)

    async def _insert_user(self, user: NewUser, token: str) -> int:
        return await BaseCRUD().insert(model=users, values=dict(email=user.email, token=token,
                                                                first_name=user.first_name, last_name=user.last_name,
                                                                calendar_id=user.calendar_id))

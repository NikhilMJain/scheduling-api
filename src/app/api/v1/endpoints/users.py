import secrets
from typing import List

from fastapi import Depends, APIRouter

from src.app.api.v1.auth import get_auth_user
from src.app.api.v1.models import UserResponse, User, NewUser
from src.app.database import users, database

router = APIRouter()


@router.get('/v1/users/', response_model=List[UserResponse])
async def get_all_users(current_user: User = Depends(get_auth_user)):
    query = users.select()
    all_users = await database.fetch_all(query)
    return all_users


@router.post('/users/')
async def add_new_user(payload: NewUser):
    token = secrets.token_hex(20)
    query = users.insert().values(email=payload.email, token=token)
    await database.execute(query)
    response_object = {
        'email': payload.email,
        'token': token
    }
    return response_object

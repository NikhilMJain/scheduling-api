import secrets

from fastapi import Depends, APIRouter
from starlette.responses import Response

from src.app.api.v1.auth import get_auth_user
from src.app.api.v1.config import API_PREFIX
from src.app.api.v1.models import UserResponse, User, NewUser
from src.app.database import database, users

router = APIRouter()


@router.get('/v1/users/{user_id}', response_model=UserResponse)
async def get_users(user_id: int = None, current_user: User = Depends(get_auth_user)):
    query = users.select().where(users.c.user_id == user_id)
    return await database.fetch_one(query)


@router.post('/v1/users/')
async def add_new_user(payload: NewUser, response: Response):
    token = secrets.token_hex(20)
    query = users.insert().values(email=payload.email, token=token, first_name=payload.first_name,
                                  last_name=payload.last_name)
    user_id = await database.execute(query)
    response_object = {
        'email': payload.email,
        'token': token
    }
    response.headers['Location'] = '{prefix}/users/{user_id}'.format(prefix=API_PREFIX, user_id=user_id)
    return response_object

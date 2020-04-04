import secrets

from fastapi import APIRouter

from src.app.api.models import UserRegistration
from src.app.database import users, database

router = APIRouter()


@router.post('/users/register/')
async def register(payload: UserRegistration):
    token = secrets.token_hex(20)
    query = users.insert().values(email=payload.email, token=token)
    await database.execute(query)
    response_object = {
        'email': payload.email,
        'token': token
    }
    return response_object

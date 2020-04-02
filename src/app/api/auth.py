from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.app.database import users, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    query = users.select().where(token == users.c.token)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return user

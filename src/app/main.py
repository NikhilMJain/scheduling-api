import secrets

import uvicorn
from fastapi import FastAPI

from src.app.api.models import UserRegistration
from src.app.database import database, metadata, engine, users

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def home():
    return {'status': 'API works'}


@app.post('/user/register/')
async def register(payload: UserRegistration):
    token = secrets.token_hex(20)
    query = users.insert().values(username=payload.username, email=payload.email, token=token)
    await database.execute(query)
    response_object = {
        'email': payload.email,
        'token': token
    }
    return response_object


if __name__== '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
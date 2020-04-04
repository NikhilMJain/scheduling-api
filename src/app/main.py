import uvicorn
from fastapi import FastAPI

from src.app.api.v1.endpoints import meetings, users, slots
from src.app.database import metadata, engine, database

metadata.create_all(engine)

app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


app.include_router(users.router)
app.include_router(meetings.router)
app.include_router(slots.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

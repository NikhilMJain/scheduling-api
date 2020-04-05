from src.app.database import database


class BaseCRUD(object):
    async def insert(self, model, values):
        query = model.insert()
        return await database.execute(query=query, values=values)

    async def bulk_insert(self, model, values):
        query = model.insert()
        return await database.execute_many(query=query, values=values)

    async def fetch(self, model, select_attributes=None, where=None):
        query = model.select(select_attributes).where(where)
        result = await database.fetch_one(query)
        return dict(result) if result else None

    async def fetch_all(self, model, select_attributes=None, where=None):
        query = model.select(select_attributes).where(where)
        return await database.fetch_all(query)

    async def update(self, model, where=None, values=None):
        query = model.update().where(where).values(values)
        return await database.execute(query)
from typing import List, Dict

from databases.backends.postgres import Record
from sqlalchemy import Table, and_

from core.app.database import database


class BaseCRUD(object):
    async def insert(self, model: Table, values: Dict) -> int:
        query = model.insert()
        return await database.execute(query=query, values=values)

    async def bulk_insert(self, model: Table, values: List[Dict]) -> None:
        query = model.insert()
        return await database.execute_many(query=query, values=values)

    async def fetch(self, model: Table, select_attributes: List[str] = None, where: and_ = None) -> Dict:
        query = model.select(select_attributes).where(where)
        result = await database.fetch_one(query)
        return dict(result) if result else None

    async def fetch_all(self, model: Table, select_attributes=None, where=None) -> List[Record]:
        query = model.select(select_attributes).where(where)
        return await database.fetch_all(query)

    async def update(self, model: Table, where: and_ = None, values: Dict = None):
        query = model.update().where(where).values(values)
        return await database.execute(query)
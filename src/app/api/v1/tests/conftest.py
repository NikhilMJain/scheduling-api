from starlette.testclient import TestClient

from src.app.database import metadata, engine
from src.app.main import app


def client():
    client = TestClient(app)
    metadata.create_all(engine)
    return client

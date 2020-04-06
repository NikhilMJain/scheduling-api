from starlette.testclient import TestClient

from core.app.database import metadata, engine
from core.app.main import app


def client():
    client = TestClient(app)
    metadata.create_all(engine)
    return client

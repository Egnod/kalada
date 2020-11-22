from motor import motor_asyncio

from kalada.core.config.database import DataBaseConfig


class Mongo:
    def __init__(self):
        self._client = motor_asyncio.AsyncIOMotorClient(DataBaseConfig.URI)
        self._db = self._client[DataBaseConfig.NAME]

    @property
    def db(self):
        return self._db

    @property
    def client(self):
        return self._client

    def close(self):
        self._client.close()

"""
    Mongoengine dependency provider extension
"""

from mongoengine.connection import (
    register_connection,
    get_db,
    DEFAULT_CONNECTION_NAME,
    disconnect
)
from nameko.extensions import DependencyProvider


class MongoEngine(DependencyProvider):
    default_connection_uri = "mongodb://localhost:27017"

    def __init__(self, alias=DEFAULT_CONNECTION_NAME):
        self.alias = alias

    def setup(self):
        config: dict = self.container.config
        mongo_uri = config.get("MONGODB_URI", self.default_connection_uri)
        register_connection(host=mongo_uri, alias=self.alias)

    def get_dependency(self, worker_ctx):
        return get_db(alias=self.alias)

    def stop(self):
        disconnect(self.alias)

    def kill(self):
        disconnect(self.alias)

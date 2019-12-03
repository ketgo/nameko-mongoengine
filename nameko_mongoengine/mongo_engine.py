"""
    Mongoengine dependency provider extension
"""

from mongoengine.connection import register_connection, disconnect, DEFAULT_CONNECTION_NAME
from nameko.extensions import DependencyProvider

from .constants import MONGODB_URI_KEY
from .database import Database


class MongoEngine(DependencyProvider):
    default_connection_uri = "mongodb://localhost:27017"

    def __init__(self):
        self.aliases = {}

    def _parse_config(self):
        config = self.container.config
        value = config.get(MONGODB_URI_KEY, self.default_connection_uri)
        self.aliases = value if isinstance(value, dict) else {DEFAULT_CONNECTION_NAME: value}

    def setup(self):
        self._parse_config()
        for alias, mongo_uri in self.aliases.items():
            register_connection(alias=alias, host=mongo_uri)

    def get_dependency(self, worker_ctx):
        return Database(DEFAULT_CONNECTION_NAME)

    def stop(self):
        for alias in self.aliases:
            disconnect(alias)

    def kill(self):
        self.stop()

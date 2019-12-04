"""
    Mongoengine dependency provider extension
"""

import json
import os

from mongoengine.connection import register_connection, disconnect, DEFAULT_CONNECTION_NAME
from nameko.extensions import DependencyProvider  # pragma: no cover

from .constants import MONGODB_URI_KEY  # pragma: no cover
from .database import Database  # pragma: no cover


class MongoEngine(DependencyProvider):
    """
        MongoEngine dependency provider for Nameko microservice framework
    """
    default_connection_uri = "mongodb://localhost:27017"

    def __init__(self):
        self.aliases = {}

    def _parse_config(self):
        config = self.container.config
        value = config.get(MONGODB_URI_KEY)
        # Check environment variables if uri not found in config file
        if not value:
            _value = os.environ.get(MONGODB_URI_KEY, self.default_connection_uri)
            # Check if aliases set in environment variable value
            try:
                value = json.loads(_value)
            except Exception:
                value = _value

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

"""
    Tests for dependency provider
"""

import json

import pytest
from mongoengine import Document, fields
from mongoengine.context_managers import switch_db
from nameko.containers import ServiceContainer
from nameko.testing.services import dummy, entrypoint_hook

from nameko_mongoengine import MongoEngine
from nameko_mongoengine.constants import MONGODB_URI_KEY


class MockModel(Document):
    meta = {"collection": "testing"}
    name = fields.StringField(required=True)


class MockService:
    name = "mock_service"
    engine = MongoEngine()

    @dummy
    def write_default(self):
        model = MockModel()
        model.name = "testing"
        model.save()

        return model

    @dummy
    def read_default(self, _id):
        rvalue = MockModel.objects.get(id=_id)

        return rvalue

    @dummy
    def get_default(self, _id):
        return self.engine.db['testing'].find_one({'_id': _id})

    @dummy
    def write_aliased(self):
        with switch_db(MockModel, "test") as NewMockModel:
            model = NewMockModel()
            model.name = "testing"
            model.save()

        return model

    @dummy
    def read_aliased(self, _id):
        with switch_db(MockModel, "test") as NewMockModel:
            rvalue = NewMockModel.objects.get(id=_id)

        return rvalue

    @dummy
    def get_aliased(self, _id):
        return self.engine.with_alias('test').db['testing'].find_one({'_id': _id})


@pytest.fixture
def config(rabbit_config):
    rabbit_config["MONGODB_URI"] = {"default": "mongomock://localhost/default", "test": "mongomock://localhost/test"}
    return rabbit_config


@pytest.fixture
def mock_container(mocker, config):
    return mocker.Mock(spec=ServiceContainer, config=config, service_name="test")


@pytest.fixture
def dependency_provider(mock_container):
    return MongoEngine().bind(mock_container, 'engine')


def test_setup(dependency_provider, config):
    dependency_provider.setup()
    assert dependency_provider.aliases == config["MONGODB_URI"]


@pytest.mark.parametrize("mongo_config, env, aliases", [
    (
            {},
            {},
            {
                "default": MongoEngine.default_connection_uri
            }
    ),
    (
            {},
            {
                MONGODB_URI_KEY: json.dumps({
                    "default": "mongodb://localhost/default_env",
                    "test": "mongodb://localhost/test_env"
                })
            },
            {
                "default": "mongodb://localhost/default_env",
                "test": "mongodb://localhost/test_env"
            }
    ),
    (
            {},
            {
                MONGODB_URI_KEY: "mongodb://localhost/default_env"
            },
            {
                "default": "mongodb://localhost/default_env"
            }
    ),
    (
            {
                MONGODB_URI_KEY: "mongodb://localhost/default_conf"
            },
            {
                MONGODB_URI_KEY: "mongodb://localhost/default_env"
            },
            {
                "default": "mongodb://localhost/default_conf"
            }
    ),
    (
            {
                MONGODB_URI_KEY: {
                    "default": "mongodb://localhost/default_conf",
                    "test": "mongodb://localhost/test_conf"
                }
            },
            {
                MONGODB_URI_KEY: "mongodb://localhost/default_env"
            },
            {
                "default": "mongodb://localhost/default_conf",
                "test": "mongodb://localhost/test_conf"
            }
    ),
    (
            {
                MONGODB_URI_KEY: {
                    "default": "mongodb://localhost/default_conf",
                    "test": "mongodb://localhost/test_conf"
                }
            },
            {
                MONGODB_URI_KEY: json.dumps({
                    "default": "mongodb://localhost/default_env",
                    "test": "mongodb://localhost/test_env"
                })
            },
            {
                "default": "mongodb://localhost/default_conf",
                "test": "mongodb://localhost/test_conf"
            }
    ),
])
def test_parse_config(mocker, mock_container, mongo_config, env, aliases):
    mocker.patch('os.environ', env)
    dep = MongoEngine().bind(mock_container, 'engine')
    dep.container.config = mongo_config
    dep._parse_config()
    assert dep.aliases == aliases


def test_end_to_end_default(container_factory, config):
    container = container_factory(MockService, config)
    container.start()

    with entrypoint_hook(container, "write_default") as write:
        model = write()
    assert model["name"] == "testing"

    model_id = model.pk
    with entrypoint_hook(container, "read_default") as read:
        model = read(model_id)
    assert model["name"] == "testing"
    assert model.pk == model_id

    with entrypoint_hook(container, "get_default") as get:
        model = get(model_id)
    assert model["name"] == "testing"
    assert model["_id"] == model_id


def test_end_to_end_aliased(container_factory, config):
    container = container_factory(MockService, config)
    container.start()

    with entrypoint_hook(container, "write_aliased") as write:
        model = write()
    assert model["name"] == "testing"

    model_id = model.pk
    with entrypoint_hook(container, "read_aliased") as read:
        model = read(model_id)
    assert model["name"] == "testing"
    assert model.pk == model_id

    with entrypoint_hook(container, "get_aliased") as get:
        model = get(model_id)
    assert model["name"] == "testing"
    assert model["_id"] == model_id

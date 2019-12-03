"""
    Tests for dependency provider
"""

import pytest
from mongoengine import Document, fields
from nameko.rpc import rpc
from nameko.testing.services import entrypoint_hook

from nameko_mongoengine import MongoEngine


class MockModel(Document):
    meta = {"collection": "testing"}
    name = fields.StringField(required=True)


class MockService:
    name = "mock_service"
    engine = MongoEngine()

    @rpc
    def write(self):
        model = MockModel()
        model.name = "testing"
        model.save()
        return model

    @rpc
    def read(self, _id):
        return MockModel.objects.get(id=_id)


@pytest.fixture
def config(rabbit_config):
    rabbit_config["MONGODB_URI"] = "mongomock://localhost"
    return rabbit_config


def test_end_to_end(container_factory, config):
    container = container_factory(MockService, config)
    container.start()

    with entrypoint_hook(container, "write") as write:
        model = write()
    assert model["name"] == "testing"

    model_id = model.pk
    with entrypoint_hook(container, "read") as read:
        model = read(model_id)
    assert model["name"] == "testing"
    assert model.pk == model_id

"""
    Test service
"""

from mongoengine import Document, fields
from mongoengine.context_managers import switch_db
from nameko.rpc import rpc

from nameko_mongoengine import MongoEngine


class MockModel(Document):
    """
        Mock mongoengine document model.
    """
    meta = {"collection": "mock"}
    name = fields.StringField(required=True)


class MockService(object):
    """
        Mock Service
    """
    name = "mock_service"
    engine = MongoEngine()

    @rpc
    def write_default(self):
        """
            Write a document defined by the `MockModel` class to the
            default database.

            See the connection URI in config.yaml for the database name.
        """
        model = MockModel()
        model.name = "testing"
        model.save()
        return str(model.id)

    @rpc
    def read_default(self, _id):
        """
            Read a document defined by the `MockModel` class from the
            default database.

            See the connection URI in config.yaml for the database name.
        """
        rvalue = MockModel.objects.get(id=_id)
        return rvalue.to_json()

    @rpc
    def write_aliased(self):
        """
            Write a document defined by the `MockModel` class to the
            aliased database.

            See the connection URI in config.yaml for the database name.
        """
        with switch_db(MockModel, "test") as NewMockModel:
            model = NewMockModel()
            model.name = "testing"
            model.save()
        return str(model.id)

    @rpc
    def read_aliased(self, _id):
        """
            Read a document defined by the `MockModel` class from the
            aliased database.

            See the connection URI in config.yaml for the database name.
        """
        with switch_db(MockModel, "test") as NewMockModel:
            rvalue = NewMockModel.objects.get(id=_id)

        return rvalue.to_json()

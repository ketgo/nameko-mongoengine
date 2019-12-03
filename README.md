# nameko-mongoengine

[![Build Status](https://travis-ci.com/ketgo/nameko-mongoengine.svg?branch=master)](https://travis-ci.com/ketgo/nameko-mongoengine)
[![codecov.io](https://codecov.io/gh/ketgo/nameko-mongoengine/coverage.svg?branch=master)](https://codecov.io/gh/ketgo/nameko-mongoengine/coverage.svg?branch=master)
[![Apache 2.0 licensed](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)
---

MongoEngine dependency provider for [Nameko](https://github.com/nameko/nameko) microservice framework.

## Installation

```bash
pip install nameko-mongoengine
```

## Usage

The basic usage of the dependency provider is shown:
```python
from mongoengine import Document, fields
from nameko_mongoengine import MongoEngine
from nameko.rpc import rpc


class MyModel(Document):
    """
        My document model
    """
    info = fields.StringField(required=True)


class MockService:
    name = "mock_service"
    engine = MongoEngine()

    @rpc
    def write(self, info):
        model = MyModel()
        model.info = info
        model.save()
        return model

    @rpc
    def read(self, _id):
        return MyModel.objects.get(id=_id)
```

The dependency `engine` exposes standard `pymongo` interface to database connection. The default `MongoEngine` database connection can be accessed by:
```python
class MockService:
    name = "mock_service"
    engine = MongoEngine()

    @rpc
    def get(self, _id):
        return self.engine.db.your_collection.find_one({'_id': _id})
```
Other database connections defined by `MongoEngine` aliases can be accessed by:
```python
@rpc
def get(self, _id):
    return self.engine.with_alias("your_alias").db.your_collection.find_one({'_id': _id})
```

## Configurations

The dependency configurations can be set in nameko `config.yaml` [file](https://docs.nameko.io/en/stable/cli.html), or by environment variables. 

### Config File

```yaml
MONGODB_URI: mongodb://localhost:27017/dbname?replicaSet=replset

# or
# ---- with aliases
MONGODB_URI:
  default: mongodb://localhost:27017/dbname?replicaSet=replset
  "<alias>": "<uri>"
```

### Environment Variables

```.env
MONGODB_URI='mongodb://localhost:27017/dbname?replicaSet=replset'

# or
# ---- with aliases
MONGODB_URI='{"default": "mongodb://localhost:27017/dbname?replicaSet=replset", "<alias>": "<uri>"}'
```

## Developers

To perform development tasks and run tests run:
```bash
$ pip install -e .[dev]			# to install all dependencies
$ docker run -d --restart=always --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management   # Run rabbitmq-management server
$ docker run --rm -d -p 27017:27017 mongo			# Run mongodb server on docker
$ pytest --cov=nameko_mongoengine tests/			# to get coverage report
$ pylint nameko_mongoengine			# to check code quality with PyLint
```
Optionally you can use `make`.

## Contributions

Pull requests always welcomed. Thanks!

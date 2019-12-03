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

The dependency provider can be used in the following way:
```python
import json

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
    def write(self, info: str) -> dict:
        model = MyModel()
        model.info = info
        model.save()
        return json.loads(model.to_json())

    @rpc
    def read(self, _id: str) -> dict:
        return MyModel.objects.get(id=_id)
```

## Configurations

The dependency configurations can be set in nameko `config.yaml` [file](https://docs.nameko.io/en/stable/cli.html), or by environment variables. 

### Config File

```yaml
MONGODB_URI: mongodb://localhost:27017/dbname?replicaSet=replset

# or
# ---- with aliases
MONGODB:
  default: mongodb://localhost:27017/dbname?replicaSet=replset
  "<alias>": "<uri>"
```

**Note:** `MONGODB` parameter overrides `MONGODB_URI`.

### Environment Variables

```.env
MONGODB_URI='mongodb://localhost:27017/dbname?replicaSet=replset'

# or
# ---- with aliases
MONGODB='{"default": "mongodb://localhost:27017/dbname?replicaSet=replset", "<alias>": "<uri>"}'
```

**Note:** `MONGODB` environment variable overrides `MONGODB_URI`.

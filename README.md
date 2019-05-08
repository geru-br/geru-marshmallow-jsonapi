marshmallow-jsonapi
===================

Marshmallow jsonapi is a ext of marshmallow to provide a default contract for GERU REST's API's


Installation
============

1. Go to directory and, install the lib

```
pip install geru.marshmallow-jsonapi
```

2. Just code with it. Inside you python app:

```
from geru.marshmallow-jsonapi import JsonApificator
```

How to use
=================

1. Define your marshmallow schema and decorate it

```python
from marshmallow import Schema, fields
from geru.marshmallow-jsonapi import JsonApificator 


@JsonApificator()
class BookSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str()

# This Schema expects a payload like:
{
    "attributtes": {
    "id": 1,
    "title": "This is my personal title"
    },
    "id": 1,
    "type": "books"
}

```

2. You can customize the default JsonApificator attributes:

```python
from marshmallow import Schema, fields, validate
from geru.marshmallow-jsonapi import JsonApificator 


@JsonApificator(id={"required": True}, type_={"validate": [validate.Length(min=8, max=200)]}, attributes={"required": True})
class BookSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str()

# This Schema expects a payload like:
{
    "attributtes": { # This is required
    "id": 1,
    "title": "This is my personal title"
    },
    "id": 1, # This is required
    "type": "books" # This is required and the min length > 8 and max length < 200
}
```


How to contribute
=================

* Assumptions:
  * Python ^2.7 or ^3.6 installed.

1. Clone the lib (and go to directory)

```
git clone https://github.com/geru-br/marshmallow-jsonapi
cd marshmallow-jsonapi
```

2. Create and activate a virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

3. Upgrade setuptools and install poetry

```
pip install --upgrade pip setuptools
pip install poetry==MANDATORY REPLACING
```

4. Install project

```
make install
```

5. Run tests

```
make test-all
```

6. Bump version

To bump a minor version, just run:

```
make bump-version
```

If you need to generate a `major`, `patch` or another different version you can read [here](https://poetry.eustace.io/docs/cli/#version) for details.


Rationale
=========

* TODO: Insert here relevant information about project's structure, concepts and operation. Get a nice example from https://github.com/geru-br/arkham/blob/master/README.md.


Credits
=======

This package was created with https://github.com/geru-br/cookiecutter-geru-pypackage project template.

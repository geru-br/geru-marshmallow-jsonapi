marshmallow-jsonapi
===================

Marshmallow jsonapi is a ext of marshmallow to provide a default contract for GERU REST's API's


Installation
============

1. Go to directory and, install the lib

```
pip install marshmallow-jsonapi
```

2. Just code with it. Inside you python app:

```
import marshmallow-jsonapi
```

* TODO: Review the Installation section


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

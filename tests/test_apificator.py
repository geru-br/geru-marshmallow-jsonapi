from .schemas import (
    BookSchemaDefault,
    BookSchemaTypeRequired,
    BookSchemaEveryoneRequired,
    BookSchemaCustomValidator,
    BookSchemaRelationship,
    BookSchemaWithTwoRelationship,
    Father,
    Child,
    Many)


class TestApificator:
    def test_default(self):
        _payload = {}
        assert BookSchemaDefault().load(_payload)

    def test_type_required(self):
        _payload = {}
        book = BookSchemaTypeRequired().load(_payload)
        assert book.errors['data']['type'] == ['Missing data for required field.']
        _payload = {
            "data": {
                "attributes": {},
                "type": "book"
            }
        }
        book = BookSchemaTypeRequired().load(_payload)
        assert book.errors == {}

    def test_everyone_required(self):
        _payload = {
            "data": {}
        }
        book = BookSchemaEveryoneRequired().load(_payload)
        assert book.errors['data']['type'] == ['Missing data for required field.']
        assert book.errors['data']['id'] == ['Missing data for required field.']
        assert book.errors['data']['attributes'] == ['Missing data for required field.']
        _payload = {
            "data": {
                "type": "book",
                "attributes": {},
                "id": ""
            }}
        book = BookSchemaEveryoneRequired().load(_payload)
        assert book.errors == {}

    def test_custom_validator(self):
        _payload = {}
        book = BookSchemaCustomValidator().load(_payload)
        assert book.errors['data']['type'] == ['Missing data for required field.']
        _payload = {
            "data": {
                "type": "books"
            }
        }
        book = BookSchemaCustomValidator().load(_payload)
        assert book.errors['data']['type'] == ['type must be book']
        _payload = {
            "data": {
                "type": "book"
            }
        }
        book = BookSchemaCustomValidator().load(_payload)
        assert book.errors == {}

    def test_one_relationship(self):
        _payload = {
            "data": {
                "relationships": {}
            }
        }
        book = BookSchemaRelationship().load(_payload)
        assert book.errors['data']['relationships']
        assert book.errors['data']['type']
        _payload = {
            "data": {
                "type": "book",
                "attributes": {
                    "title": "It"
                },
                "relationships": {
                    "author_schema": {
                        "name": "Jose"
                    }
                }
            }
        }
        book = BookSchemaRelationship().load(_payload)
        assert not book.errors

    def test_two_relationships(self):
        _payload = {
            "data": {
                "relationships": {}
            }
        }
        book = BookSchemaWithTwoRelationship().load(_payload)
        assert len(book.errors['data']['relationships']) == 1
        assert book.errors['data']['type']
        _payload = {
            "data": {
                "type": "book",
                "attributes": {
                    "title": "It"
                },
                "relationships": {
                    "author_schema": {
                        "name": "Jose"
                    },
                    "publish_schema": {
                        "name": "Martin"
                    }
                }
            }
        }
        book = BookSchemaWithTwoRelationship().load(_payload)
        assert not book.errors

    def test_inheritance(self):
        assert Father().validate({"data": {"attributes": {}}}) == {
            'data': {'attributes': {'age': [u'Missing data for required field.'],
                                    'name': [u'Missing data for required field.']}}}
        assert Child().validate({"data": {"attributes": {}}}) == {}

    def test_many_true(self):
        assert Many().validate({"data": []}) == {}
        assert Many().validate({"data": [{"name": 12345.12}]}) == {
            'data': {0: {'name': ['Not a valid string.'], 'age': ['Missing data for required field.']}}}

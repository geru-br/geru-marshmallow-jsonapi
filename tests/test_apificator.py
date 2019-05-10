from marshmallow import Schema, fields, ValidationError
from geru.marshmallow_jsonapi import JsonApificator


def must_be_book(data):
    if data != 'book':
        raise ValidationError('type must be book')


def must_be_author(data):
    if data != 'author':
        raise ValidationError('type must be author')


@JsonApificator()
class BookSchemaDefault(Schema):
    title = fields.Str()


@JsonApificator(type_={"required": True})
class BookSchemaTypeRequired(Schema):
    title = fields.Str()


@JsonApificator(id={"required": True}, type_={"required": True}, attributes={"required": True})
class BookSchemaEveryoneRequired(Schema):
    title = fields.Str()


@JsonApificator(type_={"validate": must_be_book, "required": True})
class BookSchemaCustomValidator(Schema):
    title = fields.Str()


class PublishSchema(Schema):
    name = fields.Str()


class AuthorSchema(Schema):
    name = fields.Str()


@JsonApificator(type_={"validate": must_be_book, "required": True}, relationship=[{"relationship": AuthorSchema,
                                                                                   "extra_kwargs": {"required": True}}])
class BookSchemaRelationship(Schema):
    title = fields.Str()


@JsonApificator(type_={"validate": must_be_book, "required": True}, relationship=[{"relationship": AuthorSchema,
                                                                                   "extra_kwargs": {"required": True}},
                                                                                  {"relationship": PublishSchema}])
class BookSchemaWithTwoRelationship(Schema):
    title = fields.Str()


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
                "relationship": {}
            }
        }
        book = BookSchemaRelationship().load(_payload)
        assert book.errors['data']['relationship']
        assert book.errors['data']['type']
        _payload = {
            "data": {
                "type": "book",
                "attributes": {
                    "title": "It"
                },
                "relationship": {
                    "author_schema": {
                        "name": "Jose"
                    }
                }
            }
        }
        book = BookSchemaRelationship().load(_payload)
        assert not book.errors

    def test_two_relationship(self):
        _payload = {
            "data": {
                "relationship": {}
            }
        }
        book = BookSchemaWithTwoRelationship().load(_payload)
        assert len(book.errors['data']['relationship']) == 1
        assert book.errors['data']['type']
        _payload = {
            "data": {
                "type": "book",
                "attributes": {
                    "title": "It"
                },
                "relationship": {
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

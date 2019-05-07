from marshmallow import Schema, fields, ValidationError
from marshmallow_jsonapi import JsonApificator


def must_be_book(data):
    if data != 'book':
        raise ValidationError('type must be book')


@JsonApificator()
class BookSchemaDefault(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str()


@JsonApificator(type_={"required": True})
class BookSchemaTypeRequired(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str()


@JsonApificator(id={"required": True}, type_={"required": True}, attributes={"required": True})
class BookSchemaEveryoneRequired(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str()


@JsonApificator(type_={"validate": must_be_book, "required": True})
class BookSchemaCustomValidator(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str()


class TestApificator:
    def test_default(self):
        _payload = {}
        assert BookSchemaDefault().load(_payload)

    def test_type_required(self):
        _payload = {}
        book = BookSchemaTypeRequired().load(_payload)
        assert book.errors['type'] == ['Missing data for required field.']
        _payload = {"type": "book"}
        book = BookSchemaTypeRequired().load(_payload)
        assert book.errors == {}

    def test_everyone_required(self):
        _payload = {}
        book = BookSchemaEveryoneRequired().load(_payload)
        assert book.errors['type'] == ['Missing data for required field.']
        assert book.errors['id'] == ['Missing data for required field.']
        assert book.errors['attributes'] == ['Missing data for required field.']
        _payload = {"type": "book",
                    "attributes": {},
                    "id": ''}
        book = BookSchemaEveryoneRequired().load(_payload)
        assert book.errors == {}

    def test_custom_validator(self):
        _payload = {}
        book = BookSchemaCustomValidator().load(_payload)
        assert book.errors['type'] == ['Missing data for required field.']
        _payload = {"type": "books"}
        book = BookSchemaCustomValidator().load(_payload)
        assert book.errors['type'] == ['type must be book']
        _payload = {"type": "book"}
        book = BookSchemaCustomValidator().load(_payload)
        assert book.errors == {}

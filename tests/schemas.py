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


@JsonApificator(type_={"validate": must_be_book, "required": True}, relationships=[{"relationships": AuthorSchema,
                                                                                   "extra_kwargs": {"required": True}}])
class BookSchemaRelationship(Schema):
    title = fields.Str()


@JsonApificator(type_={"validate": must_be_book, "required": True}, relationships=[{"relationships": AuthorSchema,
                                                                                   "extra_kwargs": {"required": True}},
                                                                                   {"relationships": PublishSchema}])
class BookSchemaWithTwoRelationship(Schema):
    title = fields.Str()


@JsonApificator(attributes={"required": True})
class Father(Schema):
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    cpf = fields.Str()


@JsonApificator(attributes={"required": True})
class Child(Father):
    name = fields.Str(required=False)
    age = fields.Int(required=False)


class Meta(Schema):
    count = fields.Int(dump_only=True)


class Links(Schema):
    next = fields.Str(dump_only=True)
    previous = fields.Str(dump_only=True)


@JsonApificator(many=True, other_attributes=[{"schema": Links,
                                              "name": "links",
                                              "attrs": {"many": True}},
                                             {"schema": Meta,
                                              "name": "meta"}])
class Many(Father):
    name = fields.Str(required=False)

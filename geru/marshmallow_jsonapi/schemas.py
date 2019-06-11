from marshmallow import Schema


class BaseSchema(Schema):
    """Base schema"""
    __type__ = 'path'


class QueryStringSchema(Schema):
    """Query string schemas"""
    __type__ = 'query'

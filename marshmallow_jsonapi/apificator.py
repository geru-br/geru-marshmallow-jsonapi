import marshmallow as ma

from marshmallow.class_registry import register


class JsonApificator(object):
    def __init__(self, type_={}, attributes={}, id={}):
        self._type = type_
        self._attributes = attributes
        self._id = id

    def __call__(self, cls):
        class JsonApi(ma.Schema):
            id = ma.fields.Str(**self._id)
            type = ma.fields.Str(**self._type)

            attributes = ma.fields.Nested(cls(), **self._attributes)

            def dump(self, obj, many=None):
                with_meta = dict(attributes=obj, type=cls.__name__)

                return super(JsonApi, self).dump(with_meta, many=None)

        JsonApi.orig = cls
        JsonApi.__name__ = 'JsonApi_' + cls.__name__

        register(JsonApi.__name__, JsonApi)
        return JsonApi

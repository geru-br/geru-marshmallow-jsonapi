import marshmallow as ma

from marshmallow.class_registry import register

from geru.marshmallow_jsonapi.helpers import camel_case_to_underscore


class JsonApificator(object):
    def __init__(self, type_={}, attributes={}, id={}, relationship=[]):
        self._type = type_
        self._attributes = attributes
        self._id = id
        self._relationship = relationship

    def __call__(self, cls):

        def dump(cls, obj, many=None):
            with_meta = dict(attributes=obj, type=cls.__name__)
            return super(JsonApi, self).dump(with_meta, many=None)

        json_api_fields = {
            "id": ma.fields.Str(**self._id),
            "type": ma.fields.Str(**self._type),
            "attributes": ma.fields.Nested(cls(), **self._attributes)
        }
        # If any relationship is informed, then it will be necessary to set them in Relatioship
        if self._relationship:
            relationship_fields = {}
            for relation in self._relationship:
                # Convert camel case class name to underscore pattern and then add itself in Nested field
                relationship_fields[camel_case_to_underscore(relation['relationship'].__name__)] = ma.fields.Nested(
                    relation['relationship'],
                    **relation.get(
                        'extra_kwargs', {}))
            # Create Relatioship class with its attributes
            Relationship = type('Relationship', (ma.Schema,), relationship_fields)
            json_api_fields['relationship'] = ma.fields.Nested(Relationship())

        # Create JsonApi class with its attributes
        JsonApi = type('JsonApi', (ma.Schema,), json_api_fields)
        JsonApi.dump = classmethod(dump)

        class Data(ma.Schema):
            _required = {"required": False}
            if self._type.get('required') or self._attributes.get('required') or self._id.get('required'):
                _required['required'] = True
            data = ma.fields.Nested(JsonApi, **_required)

        Data.orig = cls
        Data.__name__ = 'JsonApi_' + cls.__name__
        Data.description = 'JsonApi_' + cls.__name__
        Data.children = []
        register(Data.__name__, Data)
        return Data

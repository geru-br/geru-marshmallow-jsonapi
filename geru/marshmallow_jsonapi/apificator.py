from copy import deepcopy

import marshmallow as ma

from marshmallow.class_registry import register

from geru.marshmallow_jsonapi.helpers import camel_case_to_underscore


class JsonApificator(object):
    def __init__(self, type_={}, attributes={}, id={}, relationship=[], params_description={}, other_attributes=[],
            many=False):
        """
        JsonApificator
        :param type_: Type of schema Eg: {"required": "True"}
        :param attributes:
        :param id:
        :param relationship:
        :param params_description:
        :param other_attributes: Eg ["schema": Link, "name": "link", "attrs": {"many": True}]
        :param many:
        """
        self._type = type_
        self._attributes = attributes
        self._id = id
        self._relationship = relationship
        self._params_description = params_description
        self._many = many
        self._other_attributes = other_attributes

    def __call__(self, cls):

        def dump(cls, obj, many=None):
            with_meta = dict(attributes=obj, type=cls.__name__)
            return super(Data, self).dump(with_meta, many=None)

        cls_instance = deepcopy(cls())
        # Check if schema is an inheritance of another decorated schema with JsonApificator
        # Eg:
        #     @JsonApificator(attributes={"required": True})
        #     class Father(Schema):
        #         name = fields.Str(required=True)
        #         age = fields.Int(required=True)
        #         cpf = fields.Str()
        #
        #     @JsonApificator(attributes={"required": True})
        #     class Child(Person):
        #         name = fields.Str(required=False)
        #         age = fields.Int(required=False)
        # In this case it needs overwrite the attributes with the new attributes
        if 'data' in cls_instance.fields:
            nested = (cls_instance.fields.pop('data')).nested()
            # deepcopy is necessary to not overwrite the Father attributes schema
            old_fields = deepcopy(nested.fields['attributes'].schema.fields)
            old_fields.update(cls_instance.fields)
            cls_instance.fields = old_fields

        json_api_fields = {
            "id": ma.fields.Str(**self._id),
            "type": ma.fields.Str(**self._type),
            "attributes": ma.fields.Nested(cls_instance, **self._attributes)
        }

        # If any relationship is informed, then it will be necessary to set them into Relatioship
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

        if self._many:
            attr_pop = json_api_fields.pop('attributes')
            json_api_fields.update(attr_pop.schema.fields)
            # Create JsonApi class when many is True
            JsonApi = type('JsonApi', (ma.Schema,), json_api_fields)
        else:
            # Create JsonApi class with its attributes
            JsonApi = type('JsonApi', (ma.Schema,), json_api_fields)
        JsonApi.dump = classmethod(dump)

        class Data(ma.Schema):
            _required = {"required": False}
            if self._type.get('required') or self._attributes.get('required') or self._id.get('required'):
                _required['required'] = True
            data = ma.fields.Nested(JsonApi, many=self._many, **_required)
            # Include other attributes into Data schema
            for _attr in self._other_attributes:
                vars()[_attr['name']] = ma.fields.Nested(_attr['schema'], **_attr.get('attrs', {}))

        # Add other attributes into schema

        Data.dump = classmethod(dump)
        Data.orig = cls_instance
        Data.__name__ = 'JsonApi_' + cls.__name__
        Data.description = 'JsonApi_' + cls.__name__
        Data.children = []
        Data.params_description = self._params_description
        register(Data.__name__, Data)
        return Data

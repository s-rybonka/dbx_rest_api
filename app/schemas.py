from marshmallow import Schema
from marshmallow import ValidationError
from marshmallow import validates
from marshmallow.fields import Date
from marshmallow.fields import String


class DBoxItemSchema(Schema):
    id = String()
    name = String()
    size = String()
    path_lower = String()
    client_modified = Date()
    server_modified = Date()


class SearchQuerySchema(Schema):
    path = String(required=False)
    token = String(required=False)
    ordering = String(required=False)
    content_type = String(required=False)

    @validates('path')
    def validate_path(self, value):
        if value and not value.startswith('/'):
            raise ValidationError(
                'Query param [path] should starts from a slash (/).'
            )
        return value



from umongo import Document, fields, validate

from kalada.core.database.connector import instance


@instance.register
class CurrencyModel(Document):
    """Document model for currencies collection."""

    #  ISO Alpha3
    iso_code = fields.StringField(required=True, unique=True)
    exponent_coefficient = fields.FloatField(required=True, default=0, validate=validate.Range(min=0))
    iso_numeric_code = fields.IntField(required=True)

    class Meta:
        collection_name = "currencies"

from umongo import Document, fields, validate

from kalada.core.database.connector import instance


@instance.register
class CurrencyRateProviderModel(Document):
    """Document model for currencies collection."""

    name = fields.StringField(required=True, unique=True, validate=validate.Regexp(r"[a-z]"))
    description = fields.StringField(required=False, allow_none=True, default=None)
    official_name = fields.StringField(required=True)

    class Meta:
        collection_name = "currencies_rates_providers"

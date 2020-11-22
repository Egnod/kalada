from pymongo import ASCENDING, IndexModel
from umongo import Document, fields

from kalada.components.currency_pair.model import CurrencyPairModel
from kalada.core.database.connector import instance


@instance.register
class CurrencyPairRateModel(Document):
    """Document model for currencies collection."""

    currency_pair = fields.ReferenceField(CurrencyPairModel, required=True, allow_none=False)
    rate_date = fields.DateField(required=True)
    rate = fields.FloatField(required=True)

    class Meta:
        collection_name = "currencies_pairs_rates"
        indexes = (IndexModel([("currency_pair", ASCENDING), ("rate_date", ASCENDING)], unique=True),)

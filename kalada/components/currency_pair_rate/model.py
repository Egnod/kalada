from datetime import date, datetime
from typing import Union

from bson import ObjectId
from pymongo import ASCENDING, IndexModel
from umongo import Document, fields

from kalada.components.currency_pair.model import CurrencyPairModel
from kalada.core.database.connector import instance


@instance.register
class CurrencyPairRateModel(Document):
    """Document model for currencies collection."""

    currency_pair = fields.ReferenceField(CurrencyPairModel, required=True, allow_none=False)
    rate_date = fields.DateField(required=True)
    rate = fields.FloatField(required=False)
    is_not_found = fields.BooleanField(required=True, default=False)

    class Meta:
        collection_name = "currencies_pairs_rates"
        indexes = (IndexModel([("currency_pair", ASCENDING), ("rate_date", ASCENDING)], unique=True),)

    @classmethod
    async def fill_not_found(
        cls, currency_pair: Union[str, ObjectId, CurrencyPairModel], rate_date: date
    ) -> "CurrencyPairRateModel":
        if isinstance(rate_date, date):
            rate_date = datetime(year=rate_date.year, month=rate_date.month, day=rate_date.day)

        doc = cls(rate_date=rate_date, is_not_found=True, currency_pair=currency_pair)

        await doc.commit()

        return doc

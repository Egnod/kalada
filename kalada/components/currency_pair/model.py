from pymongo import ASCENDING, IndexModel
from umongo import Document, fields

from kalada.components.currency.model import CurrencyModel
from kalada.components.rate_provider.model import CurrencyRateProviderModel
from kalada.core.database.connector import instance


@instance.register
class CurrencyPairModel(Document):
    """Document model for currencies collection."""

    base_currency = fields.ReferenceField(CurrencyModel, required=True)
    target_currency = fields.ReferenceField(CurrencyModel, required=True)
    rate_provider = fields.ReferenceField(CurrencyRateProviderModel, required=False, allow_none=None, default=None)
    rate_provider_reverse = fields.BooleanField(required=True, default=False)
    is_active = fields.BooleanField(required=True, default=False)

    class Meta:
        collection_name = "currencies_pairs"
        indexes = (IndexModel([("base_currency", ASCENDING), ("target_currency", ASCENDING)], unique=True),)

    async def pretty_dump(self):
        dump = self.dump()

        dump["base_currency"] = (await self.base_currency.fetch()).iso_code
        dump["target_currency"] = (await self.target_currency.fetch()).iso_code
        dump["rate_provider"] = (await self.rate_provider.fetch()).official_name

        return dump

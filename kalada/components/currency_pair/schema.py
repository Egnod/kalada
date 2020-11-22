from typing import List

from pydantic import BaseModel, Field


class CurrencyPairSchema(BaseModel):
    id: str = Field(...)
    base_currency: str = Field(...)
    target_currency: str = Field(...)
    rate_provider: str = Field(...)


class CurrenciesPairsSchema(BaseModel):
    data: List[CurrencyPairSchema] = Field(default=[])

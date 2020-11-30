from datetime import date

from pydantic import BaseModel, Field


class CurrencyPairRate(BaseModel):
    base_currency: str = Field(...)
    target_currency: str = Field(...)
    rate: float = Field(...)
    rate_date: date = Field(...)

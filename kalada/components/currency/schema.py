from typing import List

from pydantic import BaseModel, Field


class CurrencySchema(BaseModel):
    id: str = Field(...)
    iso_code: str = Field(...)
    exponent_coefficient: float = Field(...)
    iso_numeric_code: int = Field(...)


class CurrenciesSchema(BaseModel):
    data: List[CurrencySchema] = Field(default=[])

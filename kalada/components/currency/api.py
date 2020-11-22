from fastapi import APIRouter

from kalada.components.currency.model import CurrencyModel
from kalada.components.currency.schema import CurrenciesSchema

router = APIRouter()


@router.get("/", response_model=CurrenciesSchema)
async def get_currencies_list() -> CurrenciesSchema:
    currencies = [currency.dump() async for currency in CurrencyModel.find({})]

    return {"data": currencies}

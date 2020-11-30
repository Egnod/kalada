from fastapi import APIRouter

from kalada.components.currency_pair.model import CurrencyPairModel
from kalada.components.currency_pair.schema import CurrenciesPairsSchema

router = APIRouter()


@router.get("/", response_model=CurrenciesPairsSchema)
async def get_currencies_pairs_list() -> CurrenciesPairsSchema:
    currencies_pairs = [await pair.pretty_dump() async for pair in CurrencyPairModel.find({"is_active": True})]

    return CurrenciesPairsSchema(date=currencies_pairs)

from datetime import date

from fastapi import APIRouter, Query

from kalada.components.currency_pair_rate.mechanism import CurrencyPairRateMechanism
from kalada.components.currency_pair_rate.schema import CurrencyPairRate

router = APIRouter()


@router.get("/daily", response_model=CurrencyPairRate)
async def get_currency_rate_daily(
    base_currency: str = Query(...), target_currency: str = Query(...)
) -> CurrencyPairRate:
    pair_rate = await CurrencyPairRateMechanism(base_currency, target_currency).load()

    return CurrencyPairRate(
        rate=await pair_rate.get_daily(),
        base_currency=base_currency,
        target_currency=target_currency,
        rate_date=date.today(),
    )


@router.get("/historical", response_model=CurrencyPairRate)
async def get_currency_rate_historical(
    base_currency: str = Query(...), target_currency: str = Query(...), rate_date: date = Query(...)
) -> CurrencyPairRate:

    pair_rate = await CurrencyPairRateMechanism(base_currency, target_currency).load()

    return CurrencyPairRate(
        rate=await pair_rate.get_by_date(rate_date),
        base_currency=base_currency,
        target_currency=target_currency,
        rate_date=rate_date.isoformat(),
    )

from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query

from kalada.components.currency.model import CurrencyModel
from kalada.components.currency_pair.model import CurrencyPairModel
from kalada.core.integrations.currency_rate import get_provider_by_identity

router = APIRouter()


@router.get("/daily")
async def get_currency_rate_daily(base_currency: str = Query(...), target_currency: str = Query(...)):
    base_currency = await CurrencyModel.find_one({"iso_code": base_currency})
    target_currency = await CurrencyModel.find_one({"iso_code": target_currency})

    if not base_currency or not target_currency:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    pair = await CurrencyPairModel.find_one({"base_currency": base_currency.id, "target_currency": target_currency.id})

    if not pair or not pair.is_active:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    provider_doc = await pair.rate_provider.fetch()

    provider = get_provider_by_identity(provider_doc.name)

    if not provider:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    async with provider() as client:
        if not pair.rate_provider_reverse:
            rate = await client.get_daily(
                base_currency.iso_code, target_currency.iso_code, reverse=pair.rate_provider_reverse
            )
        else:
            rate = await client.get_daily(
                target_currency.iso_code, base_currency.iso_code, reverse=pair.rate_provider_reverse
            )

    return rate

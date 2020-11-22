from fastapi import APIRouter

from kalada.components import currency, currency_pair, currency_pair_rate

api_router = APIRouter()

api_router.include_router(currency.router, prefix="/currencies", tags=["currencies"])
api_router.include_router(currency_pair.router, prefix="/pairs", tags=["currencies_pairs"])
api_router.include_router(currency_pair_rate.router, prefix="/rate", tags=["currencies_pairs_rates"])

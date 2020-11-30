import functools
from datetime import date, datetime
from typing import Coroutine, Optional, Type, Union

import httpx

from kalada.components.currency.exceptions import CurrencyNotFound
from kalada.components.currency.model import CurrencyModel
from kalada.components.currency_pair.exceptions import PairNotFound
from kalada.components.currency_pair.model import CurrencyPairModel
from kalada.components.currency_pair_rate.exceptions import EmptyRateByDate, PairRateMechanismNotLoaded
from kalada.components.currency_pair_rate.model import CurrencyPairRateModel
from kalada.components.rate_provider.exceptions import CurrencyRateProviderNotFound
from kalada.components.rate_provider.model import CurrencyRateProviderModel
from kalada.core.integrations.currency_rate import BaseCurrencyRateProvider, get_provider_by_identity


def loaded_mechanism_required():
    def wrapper(func):
        if isinstance(func, Coroutine):

            @functools.wraps(func)
            async def wrapped(self: "CurrencyPairRateMechanism", *args, **kwargs):
                if not self.is_loaded:
                    raise PairRateMechanismNotLoaded()

                return await func(self, *args, **kwargs)

        else:

            @functools.wraps(func)
            def wrapped(self: "CurrencyPairRateMechanism", *args, **kwargs):
                if not self.is_loaded:
                    raise PairRateMechanismNotLoaded()

                return func(self, *args, **kwargs)

        return wrapped

    return wrapper


class CurrencyPairRateMechanism:
    def __init__(self, base_currency: str, target_currency: str, session: Optional[httpx.AsyncClient] = None):
        self.base_currency = base_currency
        self.target_currency = target_currency

        self._loaded: bool = False
        self._base_currency_doc: Optional[CurrencyModel] = None
        self._target_currency_doc: Optional[CurrencyModel] = None
        self._pair_doc: Optional[CurrencyPairModel] = None
        self._provider_doc: Optional[CurrencyRateProviderModel] = None
        self._provider: Optional[Type[BaseCurrencyRateProvider]] = None
        self._rate_date: Optional[datetime] = None

        self.__session = session

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    @property
    @loaded_mechanism_required()
    def pair_document(self) -> CurrencyPairModel:
        return self._pair_doc

    async def load(self) -> "CurrencyPairRateMechanism":
        self._base_currency_doc = await CurrencyModel.find_one({"iso_code": self.base_currency})
        self._target_currency_doc = await CurrencyModel.find_one({"iso_code": self.target_currency})

        if not self._base_currency_doc:
            raise CurrencyNotFound(self.base_currency)
        elif not self._target_currency_doc:
            raise CurrencyNotFound(self.target_currency)

        self._pair_doc = await CurrencyPairModel.find_one(
            {"base_currency": self._base_currency_doc.id, "target_currency": self._target_currency_doc.id}
        )

        if not self._pair_doc or not self._pair_doc.is_active:
            raise PairNotFound(self.base_currency, self.target_currency)

        self._provider_doc = await self._pair_doc.rate_provider.fetch()

        self._provider = get_provider_by_identity(self._provider_doc.name)

        if not self._provider:
            raise CurrencyRateProviderNotFound(self._provider_doc.name)

        self._loaded = True

        return self

    async def _get_daily_provided(self):
        async with self._provider(session=self.__session) as client:
            if not self._pair_doc.rate_provider_reverse:
                rate = await client.get_daily(
                    self.base_currency, self.target_currency, reverse=self._pair_doc.rate_provider_reverse
                )
            else:
                rate = await client.get_daily(
                    self.target_currency, self.base_currency, reverse=self._pair_doc.rate_provider_reverse
                )

        return rate

    async def _get_by_date_provided(self):
        async with self._provider(session=self.__session) as client:
            if not self._pair_doc.rate_provider_reverse:
                rate = await client.get_historical_rate(
                    self.base_currency,
                    self.target_currency,
                    rate_date=self._rate_date.date(),
                    reverse=self._pair_doc.rate_provider_reverse,
                )
            else:
                rate = await client.get_historical_rate(
                    self.target_currency,
                    self.base_currency,
                    rate_date=self._rate_date.date(),
                    reverse=self._pair_doc.rate_provider_reverse,
                )

        return rate

    async def _get_cached_rate(self) -> Optional[CurrencyPairRateModel]:
        rate_doc = await CurrencyPairRateModel.find_one(
            {"rate_date": self._rate_date, "currency_pair": self._pair_doc.id}
        )

        return rate_doc

    async def _set_cached_rate(self, rate: Union[int, float]):
        await CurrencyPairRateModel(rate_date=self._rate_date, currency_pair=self._pair_doc, rate=rate).commit()

    @loaded_mechanism_required()
    async def get_by_date(self, rate_date: date):
        if isinstance(rate_date, date):
            rate_date = datetime(rate_date.year, rate_date.month, rate_date.day)

        self._rate_date = rate_date

        rate = await self._get_cached_rate()

        if not rate:
            rate = await self._get_by_date_provided()

            if rate is None:
                raise EmptyRateByDate()

            await self._set_cached_rate(rate)
        else:
            rate = rate.rate

        return rate

    @loaded_mechanism_required()
    async def get_daily(self) -> Optional[Union[float, int]]:
        self._rate_date = datetime(date.today().year, date.today().month, date.today().day)

        rate = await self._get_cached_rate()

        if not rate:
            rate = await self._get_daily_provided()

            if rate is None:
                raise EmptyRateByDate()

            await self._set_cached_rate(rate)
        else:
            rate = rate.rate

        return rate

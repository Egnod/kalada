from datetime import date
from typing import Optional, Union
from urllib.parse import urljoin

import xmltodict
from iso4217 import Currency as currencies

from kalada.core.integrations.currency_rate.base import BaseCurrencyRateProvider


class RussiaBankProviderRate(BaseCurrencyRateProvider):
    identity = "cbr"
    official_name = "The Central Bank of the Russian Federation"
    description = (
        "The Central Bank of the Russian Federation is the main issuing bank and monetary regulator of the country."
    )

    _base_url = "http://www.cbr.ru/scripts/"

    currency_pairs_compatibility = {
        currencies.rub.code: (currencies.usd.code, currencies.eur.code),
    }

    denomination = {date(year=1998, day=1, month=1): 1000}

    async def set_denomination(self, rate_date: date, rate: float, reverse: bool = False):
        for denomination_date in self.denomination:
            if rate_date < denomination_date:
                if rate:
                    if reverse:
                        rate *= self.denomination[denomination_date]
                    else:
                        rate /= self.denomination[denomination_date]

        return rate

    async def get_historical_rate(
        self, base_currency: str, target_currency: str, rate_date: date, reverse: bool = False
    ) -> Optional[Union[int, float]]:
        url = urljoin(self._base_url, "XML_daily.asp")

        response = await self.session.get(
            url,
            params={"date_req": rate_date.strftime("%d/%m/%Y")},
        )

        data = response.text

        data = xmltodict.parse(data)

        wallets = data["ValCurs"]["Valute"]

        rate = None

        for currency in wallets:
            if currency["CharCode"] == target_currency:
                rate = float(currency["Value"].replace(",", "."))
                rate = (
                    await self.set_denomination(rate_date, rate)
                    if reverse
                    else await self.set_denomination(rate_date, 1 / rate, True)
                )

        return rate

    async def get_daily(self, base_currency: str, target_currency: str, reverse: bool = False):
        url = urljoin(self._base_url, "XML_daily.asp")

        response = await self.session.get(
            url,
            params={"date_req": date.today().strftime("%d/%m/%Y")},
        )

        data = response.text

        data = xmltodict.parse(data)

        wallets = data["ValCurs"]["Valute"]

        rate = None

        for currency in wallets:
            if currency["CharCode"] == target_currency:
                rate = float(currency["Value"].replace(",", "."))
                rate = rate if reverse else 1 / rate

        return rate

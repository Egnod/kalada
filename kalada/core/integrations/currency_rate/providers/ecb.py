from datetime import date
from typing import Optional, Union
from urllib.parse import urljoin

from iso4217 import Currency as currencies

from kalada.core.integrations.currency_rate import BaseCurrencyRateProvider


class EuropeanBankProvider(BaseCurrencyRateProvider):
    _base_url = "https://api.exchangeratesapi.io/"
    official_name = "The European Central Bank"
    description = (
        "The European Central Bank (ECB) is the central bank of the Eurozone,"
        " a monetary union of 19 EU member states which employ the euro."
    )
    currency_pairs_compatibility = {
        currencies.usd.code: (currencies.eur.code,),
        currencies.eur.code: (currencies.usd.code,),
        currencies.gbp.code: (currencies.usd.code, currencies.eur.code),
    }

    identity = "ecb"

    async def get_daily(
        self,
        base_currency: str,
        target_currency: str,
        reverse: bool = False,
    ):

        url = urljoin(self._base_url, "latest")
        response = await self.session.get(url, params={"base": base_currency})
        data = response.json()

        wallets = data["rates"]

        rates = {}

        for wallet in wallets:
            rates[wallet] = wallets[wallet]

        return rates[target_currency] if not reverse else (1 / rates[target_currency])

    async def get_historical_rate(
        self, base_currency: str, target_currency: str, rate_date: date, reverse: bool = False
    ) -> Optional[Union[int, float]]:
        url = urljoin(self._base_url, rate_date.isoformat())

        response = await self.session.get(url, params={"base": base_currency})

        data = response.json()

        wallets = data["rates"]

        rates = {}

        for wallet in wallets:
            rates[wallet] = wallets[wallet]

        return rates[target_currency] if not reverse else (1 / rates[target_currency])

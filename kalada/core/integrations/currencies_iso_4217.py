from urllib.parse import urljoin

import pandas as pd
import xmltodict
from loguru import logger

from kalada.core.integrations.base import BaseHTTPIntegration


class CurrencyProvider(BaseHTTPIntegration):
    identity = "iso_4217"
    _base_url = "https://www.currency-iso.org/"

    @logger.catch
    async def get_currencies_list(self, path: str = "dam/downloads/lists/list_one.xml") -> pd.DataFrame:
        response = await self.session.get(urljoin(self._base_url, path))
        structure = xmltodict.parse(response.text)["ISO_4217"]["CcyTbl"]["CcyNtry"]

        df = pd.DataFrame(structure)
        df.columns = ["Country", "CurrencyName", "CurrencyCode", "CurrencyNumericCode", "CurrencyUnits"]
        df.drop_duplicates(subset=["CurrencyCode"], inplace=True)

        del df["CurrencyName"]
        del df["Country"]

        df = df.loc[df["CurrencyUnits"] != "N.A."]
        df = df.dropna()

        return df

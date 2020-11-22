from abc import ABCMeta, abstractmethod
from datetime import date
from typing import Dict, Optional, Tuple, Union

from kalada.core.integrations.base import BaseHTTPIntegration


class BaseCurrencyRateProvider(BaseHTTPIntegration, metaclass=ABCMeta):
    @property
    @abstractmethod
    def currency_pairs_compatibility(self) -> Dict[str, Tuple[str]]:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def official_name(self) -> str:
        pass

    @abstractmethod
    async def get_daily(
        self, base_currency: str, target_currency: str, reverse: bool = False
    ) -> Optional[Union[int, float]]:
        pass

    @abstractmethod
    async def get_historical_rate(
        self, base_currency: str, target_currency: str, rate_date: date, reverse: bool = False
    ) -> Optional[Union[int, float]]:
        pass

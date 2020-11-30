from kalada.core.exception import KaladaException


class KaladaCurrencyPairException(KaladaException):
    pass


class PairNotFound(KaladaCurrencyPairException):
    def __init__(self, base_currency: str, target_currency: str):
        self._base_currency = base_currency
        self._target_currency = target_currency

    def __str__(self):
        return f"Pair {self._base_currency}/{self._target_currency} not found"

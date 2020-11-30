from kalada.core.exception import KaladaException


class KaladaCurrencyException(KaladaException):
    pass


class CurrencyNotFound(KaladaCurrencyException):
    def __init__(self, base_currency: str):
        self._base_currency = base_currency

    def __str__(self):
        return f"Currency {self._base_currency} not found"

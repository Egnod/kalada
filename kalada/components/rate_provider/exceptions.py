from kalada.core.exception import KaladaException


class KaladaCurrencyRateProviderException(KaladaException):
    pass


class CurrencyRateProviderNotFound(KaladaCurrencyRateProviderException):
    def __init__(self, provider_identity: str):
        self._provider_identity = provider_identity

    def __str__(self):
        return f"Provider {self._provider_identity} not found"

from typing import List, Tuple, Type

from loguru import logger

from kalada.core.integrations.currency_rate import BaseCurrencyRateProvider


def get_all_providers() -> List[Type[BaseCurrencyRateProvider]]:
    return BaseCurrencyRateProvider.__subclasses__()


def get_provider_by_identity(identity: str) -> Type[BaseCurrencyRateProvider]:
    for provider in BaseCurrencyRateProvider.__subclasses__():
        if provider.identity == identity:
            return provider


def get_provider_by_currency(base_currency: str, target_currency: str) -> Tuple[Type[BaseCurrencyRateProvider], bool]:
    providers: List[Type[BaseCurrencyRateProvider]] = get_all_providers()

    reverse = False
    for provider in providers:
        if (
            base_currency in provider.currency_pairs_compatibility
            and target_currency in provider.currency_pairs_compatibility[base_currency]
        ) or (
            reverse := (
                target_currency in provider.currency_pairs_compatibility
                and base_currency in provider.currency_pairs_compatibility[target_currency]
            )
        ):
            return provider, reverse

    logger.warning(f"Provider not found! {base_currency} -> {target_currency} | reverse={reverse}")

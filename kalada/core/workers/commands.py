from itertools import permutations

from loguru import logger

from kalada.components.currency.model import CurrencyModel
from kalada.components.currency_pair.model import CurrencyPairModel
from kalada.components.currency_pair_rate.model import CurrencyPairRateModel
from kalada.components.rate_provider.model import CurrencyRateProviderModel
from kalada.core.integrations.currencies_iso_4217 import CurrencyProvider
from kalada.core.integrations.currency_rate import get_all_providers, get_provider_by_currency
from kalada.core.workers.app import get_app

app = get_app()


@app.command()
async def currencies_sync():
    """Sync currencies collection."""
    async with CurrencyProvider() as provider:
        df = await provider.get_currencies_list()

        df.columns = ["iso_code", "iso_numeric_code", "exponent_coefficient"]

        currencies = df.to_dict("records")

        for currency in currencies:
            try:
                await CurrencyModel(**currency).commit()
            except Exception:
                logger.opt(exception=True, colors=True).warning(
                    "Collect currency {iso_code} warning", iso_code=currency["iso_code"]
                )


@app.command()
async def generate_pairs_combinations():
    """Generate all currency pairs combinations."""

    currencies = [currency async for currency in CurrencyModel.find({})]

    currency_pairs = list(permutations(currencies, 2))

    for pair in currency_pairs:
        await CurrencyPairModel(base_currency=pair[0], target_currency=pair[1]).commit()


@app.command()
async def ensure_indexes_collections():
    """Ensure all indexes for collections."""

    for model in [CurrencyPairModel, CurrencyModel, CurrencyRateProviderModel, CurrencyPairRateModel]:
        await model.ensure_indexes()


@app.command()
async def collect_currency_rates_providers():
    """Collect currency rates from code."""

    providers = get_all_providers()

    for provider in providers:
        if not (await CurrencyRateProviderModel.find_one({"name": provider.identity})):
            await CurrencyRateProviderModel(
                name=provider.identity, description=provider.description, official_name=provider.official_name
            ).commit()


@app.command()
async def select_provider_and_activate():
    """Select provider for currency pair and active if provider exists."""

    async for pair in CurrencyPairModel.find({}):
        base_currency = (await pair.base_currency.fetch()).iso_code
        target_currency = (await pair.target_currency.fetch()).iso_code

        provider = get_provider_by_currency(base_currency, target_currency)

        if provider is not None:
            provider, is_reverse = provider
            provider_doc = await CurrencyRateProviderModel.find_one({"name": provider.identity})

            pair.is_active = True
            pair.rate_provider = provider_doc
            pair.rate_provider_reverse = is_reverse

            await pair.commit()


@app.command()
async def full_deploy():
    """Collect all and select providers for currencies pairs."""

    await ensure_indexes_collections.run()
    await currencies_sync.run()
    await generate_pairs_combinations.run()
    await collect_currency_rates_providers.run()
    await select_provider_and_activate.run()

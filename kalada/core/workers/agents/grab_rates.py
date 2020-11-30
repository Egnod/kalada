from datetime import date
from typing import AsyncIterable

import httpx
from faust import StreamT
from loguru import logger

from kalada.components.currency_pair_rate.exceptions import EmptyRateByDate
from kalada.components.currency_pair_rate.mechanism import CurrencyPairRateMechanism
from kalada.components.currency_pair_rate.model import CurrencyPairRateModel
from kalada.core.config.workers import WorkersConfig
from kalada.core.workers.agents import app
from kalada.core.workers.records import GrabRateByDate

grab_rate_topic = app.topic("grab_rate", internal=True, value_type=GrabRateByDate, partitions=WorkersConfig.MAX_CLIENTS)


@app.agent(grab_rate_topic, concurrency=WorkersConfig.agents.GRAB_RATES_CONCURRENCY)
@logger.catch
async def grab_rate_collect(
    stream: StreamT[GrabRateByDate],
) -> AsyncIterable[bool]:
    async with httpx.AsyncClient() as session:
        async for event in stream:
            logger.info(
                "Collect {base_currency}/{target_currency}/{rate_date}",
                base_currency=event.base_currency,
                target_currency=event.target_currency,
                rate_date=event.rate_date,
            )

            pair_rate = await CurrencyPairRateMechanism(
                event.base_currency, event.target_currency, session=session
            ).load()
            rate_date = date.fromisoformat(event.rate_date)

            try:
                await pair_rate.get_by_date(rate_date=rate_date)
            except EmptyRateByDate:
                logger.opt(exception=True).warning(
                    "Fail get rate for {base_currency}/{target_currency} pair for {rate_date}",
                    base_currency=event.base_currency,
                    target_currency=event.target_currency,
                    rate_date=event.rate_date,
                )

                await CurrencyPairRateModel.fill_not_found(pair_rate.pair_document.id, rate_date)
            except Exception:
                logger.opt(exception=True).exception("?")

            yield True

from datetime import date

from dateutil.relativedelta import relativedelta

from kalada.components.currency_pair.model import CurrencyPairModel
from kalada.core.workers.agents import grab_rate_collect
from kalada.core.workers.records import GrabRateByDate


async def full_grab_for_all_pairs(start_date: date = date(year=2000, month=1, day=1), due_date=date.today()) -> None:
    pairs = [await pair.pretty_dump() async for pair in CurrencyPairModel.find({"is_active": True})]

    for pair in pairs:
        current_date = start_date

        while current_date != due_date:
            await grab_rate_collect.send(
                value=GrabRateByDate(
                    base_currency=pair["base_currency"],
                    target_currency=pair["target_currency"],
                    rate_date=current_date.isoformat(),
                )
            )

            current_date += relativedelta(days=1)

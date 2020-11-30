from faust import Record


class GrabRateByDate(Record):
    base_currency: str
    target_currency: str
    rate_date: str

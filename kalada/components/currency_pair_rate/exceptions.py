from kalada.core.exception import KaladaException


class KaladaCurrencyPairRateException(KaladaException):
    pass


class PairRateMechanismNotLoaded(KaladaCurrencyPairRateException):
    pass


class EmptyRateByDate(KaladaCurrencyPairRateException):
    pass

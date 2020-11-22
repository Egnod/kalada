import faust

from kalada import __project__
from kalada.core.config.workers import WorkersConfig


def get_app():
    app = faust.App(
        __project__,
        broker=WorkersConfig.KAFKA_SERVER_URI,
        broker_check_crcs=False,
        topic_partitions=WorkersConfig.MAX_CLIENTS,
        producer_max_request_size=WorkersConfig.PRODUCER_MAX_REQUEST_SIZE,
        consumer_max_fetch_size=WorkersConfig.CONSUMER_MAX_FETCH_SIZE,
    )

    return app

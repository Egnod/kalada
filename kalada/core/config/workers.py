from kalada.core.config.configurator import configurator


class WorkersConfig:
    KAFKA_SERVER_URI = configurator.get_config("workers_kafka_server_uri", path_mode=True)
    PRODUCER_MAX_REQUEST_SIZE = int(configurator.get_config("workers_producer_request_size_max", path_mode=True))
    CONSUMER_MAX_FETCH_SIZE = int(configurator.get_config("workers_consumer_fetch_size_max", path_mode=True))
    MAX_CLIENTS = int(configurator.get_config("workers_clients_max", path_mode=True))

    class agents:
        GRAB_RATES_CONCURRENCY = int(
            configurator.get_config("workers_agents_grabrate_concurrency", default=1, path_mode=True)
        )

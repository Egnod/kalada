from kalada.core.config.configurator import configurator


class WorkersConfig:
    KAFKA_SERVER_URI = configurator.get_config("workers_kafka_server_uri", path_mode=True)
    PRODUCER_MAX_REQUEST_SIZE = configurator.get_config("workers_producer_request_size_max", path_mode=True)
    CONSUMER_MAX_FETCH_SIZE = configurator.get_config("workers_consumer_fetch_size_max", path_mode=True)
    MAX_CLIENTS = configurator.get_config("workers_clients_max", path_mode=True)

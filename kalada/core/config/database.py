from kalada.core.config.configurator import configurator


class DataBaseConfig:
    URI = configurator.get_config("database_uri", path_mode=True)
    NAME = configurator.get_config("database_name", path_mode=True)

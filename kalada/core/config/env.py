from enum import Enum

from kalada.core.config.configurator import configurator


class Environments(Enum):
    production = "production"
    develop = "develop"

    @classmethod
    def get_envs(cls):
        return list(cls.__members__.keys())


ENV = configurator.get_config("env", default="develop")

if ENV not in Environments.get_envs():
    raise ValueError(f"Incorrect environment '{ENV}'. Supported environments: {Environments.get_envs()}")

IS_PRODUCTION = ENV == Environments.production.value

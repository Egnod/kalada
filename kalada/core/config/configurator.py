from sitri import Sitri
from sitri.contrib.system import SystemConfigProvider
from sitri.contrib.yaml import YamlConfigProvider
from sitri.strategy.index_priority import IndexPriorityStrategy

from kalada import __project__

configurator = Sitri(
    config_provider=IndexPriorityStrategy(
        SystemConfigProvider(prefix=__project__),
        YamlConfigProvider(default_separator="_", yaml_path="./config.yaml", found_file_error=False),
    )
)

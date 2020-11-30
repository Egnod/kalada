from kalada.core.workers.app import get_app

app = get_app()

from kalada.core.workers.agents.grab_rates import grab_rate_collect  # noqa # isort:skip

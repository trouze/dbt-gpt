from dbt.adapters.gpt.connections import GptConnectionManager # noqa
from dbt.adapters.gpt.connections import GptCredentials
from dbt.adapters.gpt.impl import GptAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import gpt


Plugin = AdapterPlugin(
    adapter=GptAdapter,
    credentials=GptCredentials,
    include_path=gpt.PACKAGE_PATH
    )

from dataclasses import dataclass
from typing import Optional
from dbt.adapters.base import BaseAdapter as adapter_cls
from dbt.adapters.base.impl import AdapterConfig
from dbt.adapters.gpt import GptConnectionManager

@dataclass
class GptConfig(AdapterConfig):
    model: Optional[str] = None


class GptAdapter(adapter_cls):
    """
    Controls actual implmentation of adapter, and ability to override certain methods.
    """

    ConnectionManager = GptConnectionManager
    AdapterSpecificConfigs = GptConfig

    @classmethod
    def date_function(cls):
        """
        Returns canonical date func
        """
        return """
        import datetime
        return datetime.datetime.now()
        """

 # may require more build out to make more user friendly to confer with team and community.

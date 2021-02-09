from typing import Dict, Callable

from app.data.source.rancher import RancherDatasource
from app.data.source.gke import GkeDataSource

class SourceRegister:
    sources: Dict[str, Callable] = {
        'rancher': RancherDatasource,
        'gke': GkeDataSource
    }

    @classmethod
    def find_source(cls, source_name: str) -> Callable:
        return cls.sources.get(source_name)

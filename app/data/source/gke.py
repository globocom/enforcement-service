from typing import List, Dict
import requests

from app.data.source.definition.base import BaseSource
from app.domain.entities import Cluster


class GkeDataSource(BaseSource):
    def get_clusters(self) -> List[Cluster]:
       url = f"{self.config.gcp_url}/v1/projects/*/locations/*/clusters"

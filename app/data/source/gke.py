from typing import List, Dict

from app.data.source.definition.base import BaseSource
from app.domain.entities import Cluster
from google.oauth2 import service_account

class GkeDataSource(BaseSource):
    def get_clusters(self) -> List[Cluster]:
       url = f"{self.config.gcp_url}/v1/projects/*/locations/*/clusters"

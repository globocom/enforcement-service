import json
from typing import List, Any, Dict

from google.cloud.container import ClusterManagerClient
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

from app.data.source.definition.base import BaseSource
from app.domain.entities import Cluster


class GkeDataSource(BaseSource):
    def get_clusters(self) -> List[Cluster]:
        project_id = self._get_service_account_or_field("project_id")
        client = self._get_client()

        response = client.list_clusters(project_id=project_id, zone='-')
        return self._filter_and_map_clusters(
            response.clusters, self.source.gke.labels, self.source.gke.ignore
        )

    def _filter_and_map_clusters(self, clusters_list: List[Dict],
                                 labels: dict, ignore: List[str]) -> List[Cluster]:
        return list(
            map(
                self._build_cluster,
                filter(
                    lambda cluster_map: self._filter_cluster(cluster_map, labels, ignore),
                    clusters_list
                )
            )
        )

    @classmethod
    def _filter_cluster(cls, cluster_map: dict, labels: dict, ignore: List[str]) -> bool:
        if ignore and cluster_map.name in ignore:
            return False

        return set(labels.items()).issubset(set(cluster_map.resource_labels.items())) if labels else True

    @classmethod
    def _build_cluster(cls, cluster: Any) -> Cluster:
        return Cluster(
            name=cluster.name,
            id=cluster.name,
            token=cluster.token,
            url=f'https://{cluster.endpoint}',
        )

    def _get_credentials(self) -> Credentials:
        sa = self._get_service_account_or_field()
        credentials = service_account.Credentials.from_service_account_info(sa)
        return credentials

    def _get_client(self) -> ClusterManagerClient:
        credentials = self._get_credentials()
        return ClusterManagerClient(credentials=credentials)

    def _get_service_account_or_field(self, field: str = None) -> Any:
        sa = json.loads(self.secret['key.json'])
        if field is None:
            return sa
        return sa.get(field)

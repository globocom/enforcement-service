from typing import List, Dict

import requests

from app.data.source.definition.base import BaseSource
from app.domain.entities import Cluster

class RancherDatasource(BaseSource):
    def get_clusters(self) -> List[Cluster]:
        secret_decoded = self.kubernetes_helper.get_secret_and_return_decoded(self.source, 'rancher')
        self.config.rancher_token = secret_decoded.get('password')
        self.config.rancher_url = secret_decoded.get('url')

        headers = {
            "Authorization": f"Bearer {self.config.rancher_token}"
        }

        filters: dict = self.source.rancher.filters if self.source.rancher.filters else dict()
        filters.update({'state': 'active'})

        url = f"{self.config.rancher_url}/v3/clusters"

        with requests.get(
            url, verify=False, headers=headers, params=filters, timeout=5,
        ) as response:
            response.raise_for_status()
            return self._filter_and_map_clusters(
                response.json()['data'], self.source.rancher.labels, self.source.rancher.ignore
            )

    def _filter_and_map_clusters(self, clusters_list: List[Dict], labels: dict, ignore: List[str]) -> List[Cluster]:
        return list(
                    map(
                        self._build_cluster,
                        filter(
                            lambda cluster_map: self._filter_cluster(cluster_map, labels, ignore),
                            clusters_list
                        )
                    )
        )

    def _filter_cluster(self, cluster_map: dict, labels: dict, ignore: List[str]) -> bool:
        if ignore and cluster_map['name'] in ignore:
            return False

        return set(labels.items()).issubset(set(cluster_map['labels'].items())) if labels else True

    def _build_cluster(self, cluster_map: dict) -> Cluster:
        return Cluster(
            name=cluster_map['name'],
            id=cluster_map['id'],
            token=self.config.rancher_token,
            url=f'{self.config.rancher_url}/k8s/clusters/{cluster_map["id"]}',
        )




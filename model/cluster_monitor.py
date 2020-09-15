from injector import inject
from dataclasses import dataclass
from typing import List


from data import RancherRepository, ArgoRepository
from model.cluster import Cluster
from model.cluster_factory import ClusterFactory


@inject
@dataclass
class ClusterMonitor:
    _rancher_repository: RancherRepository
    _argo_repository: ArgoRepository
    _cluster_factory: ClusterFactory

    def __post_init__(self):
        self._rancher_clusters = self._rancher_repository.get_clusters()
        self._argo_clusters_info = self._argo_repository.list_clusters_info()

    def detect_new_clusters(self) -> List[Cluster]:

        return list(
            map(
                lambda cluster_map: self._cluster_factory.create(cluster_map),
                filter(
                    lambda cluster: cluster['name'] not in self._argo_clusters_info,
                    self._rancher_clusters
                )
            )
        )

    def detect_deleted_clusters(self) -> List[Cluster]:

        clusters_map = {cluster['name']: cluster for cluster in self._rancher_clusters}

        return list(
            map(
                lambda cluster_info: self._cluster_factory.create(cluster_info),
                filter(
                    lambda cluster_info: cluster_info["name"] not in clusters_map,
                    self._argo_clusters_info
                )
            )
        )

    def register(self, cluster: Cluster):
        self._argo_repository.register_cluster(cluster)

    def unregister(self, cluster):
        if cluster.name != 'in-cluster':
            self._argo_repository.unregister_cluster(cluster)

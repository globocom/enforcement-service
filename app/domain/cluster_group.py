from __future__ import annotations

from typing import List

import attr

from app.domain.entities import Cluster
from app.domain.repositories import ClusterRepository, ProjectRepository


@attr.s(auto_attribs=True)
class ClusterGroup:
    _clusters: List[Cluster]
    _cluster_repository: ClusterRepository
    _project_repository: ProjectRepository

    @property
    def clusters(self):
        return self._clusters

    def register(self):
        for cluster in self._clusters:
            self._cluster_repository.register_cluster(cluster)
            self._project_repository.create_project(cluster)

    def unregister(self):
        for cluster in self._clusters:
            self._cluster_repository.unregister_cluster(cluster)
            self._project_repository.remove_project(cluster.name)

    def __sub__(self, other: ClusterGroup) -> ClusterGroup:
        cluster_names = {cluster.name: cluster for cluster in other.clusters}
        result_clusters = list(
            filter(
                lambda cluster: cluster.name not in cluster_names,
                self._clusters
            )
        )

        return ClusterGroup(cluster_repository=self._cluster_repository
                            , project_repository=self._project_repository,
                            clusters=result_clusters)

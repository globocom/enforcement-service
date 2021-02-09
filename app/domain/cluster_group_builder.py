from typing import List

import attr

from app.domain.cluster_group import ClusterGroup
from app.domain.entities import Cluster
from app.domain.repositories import ClusterRepository, ProjectRepository


@attr.s(auto_attribs=True)
class ClusterGroupBuilder:
    _cluster_repository: ClusterRepository
    _project_repository: ProjectRepository

    def build(self, clusters: List[Cluster]) -> ClusterGroup:
        return ClusterGroup(clusters=clusters,
                            cluster_repository=self._cluster_repository,
                            project_repository=self._project_repository)

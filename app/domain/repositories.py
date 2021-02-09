from typing import List, Dict, Any

from app.domain.entities import Cluster, Enforcement


class ClusterRepository:
    def list_clusters_info(self) -> List[Dict[str, str]]:
        raise Exception("Not implemented")

    def unregister_cluster(self, cluster: Cluster) -> None:
        raise Exception("Not implemented")

    def register_cluster(self, cluster: Cluster) -> None:
        raise Exception("Not implemented")


class EnforcementRepository:
    def create_enforcement(self, cluster_name: str, instance_name: str, enforcement: Enforcement) -> None:
        raise Exception("Not implemented")

    def update_enforcement(self, cluster_name: str, instance_name: str, enforcement: Enforcement) -> None:
        raise Exception("Not implemented")

    def remove_enforcement(self, enforcement_name: str) -> None:
        raise Exception("Not implemented")

    def list_installed_enforcements(self, **filters: Any) -> List[Enforcement]:
        raise Exception("Not implemented")


class SourceRepository:
    def get_clusters(self) -> List[Cluster]:
        raise Exception('Not implement')


class ProjectRepository:
    def create_project(self, cluster: Cluster) -> None:
        raise Exception("Not implemented")

    def remove_project(self, project_name: str) -> None:
        raise Exception("Not implemented")




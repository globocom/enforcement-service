import attr
from argocd_client import ProjectServiceApi

from app.domain.entities import Cluster
from app.domain.repositories import ProjectRepository


@attr.s(auto_attribs=True)
class ProjectService(ProjectRepository):
    _project_service: ProjectServiceApi

    def create_project(self, cluster: Cluster) -> None:
        body = {
            'project': {
                'metadata': {
                    'name': cluster.name
                },
                'spec': {
                    'destinations': [{'server': cluster.url, 'namespace': '*'}],
                    'sourceRepos': ['*'],
                    'clusterResourceBlacklist': [],
                    'clusterResourceWhitelist': [],
                    'namespaceResourceBlacklist': [],
                    'namespaceResourceWhitelist': [],
                    'orphanedResources': None,
                    'roles': [],
                    'signatureKeys': [],
                    'syncWindows': []
                }
            },
            "upsert": True
        }

        self._project_service.create_mixin6(body)

    def remove_project(self, project_name: str) -> None:
        self._project_service.delete_mixin6(name=project_name)

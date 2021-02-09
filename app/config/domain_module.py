from injector import Module, provider, singleton

from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_change_detector_builder import EnforcementChangeDetectorBuilder
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.repositories import ClusterRepository, ProjectRepository, EnforcementRepository


class DomainModule(Module):

    @provider
    @singleton
    def provide_cluster_group_builder(self, cluster_repository: ClusterRepository,
                                      project_repository: ProjectRepository) -> ClusterGroupBuilder:
        return ClusterGroupBuilder(cluster_repository=cluster_repository, project_repository=project_repository)

    @provider
    @singleton
    def provide_enforcement_installer_builder(self,
                                              enforcement_repository: EnforcementRepository) -> EnforcementInstallerBuilder:
        return EnforcementInstallerBuilder(enforcement_repository=enforcement_repository)

    @provider
    @singleton
    def provide_enforcement_change_detector_builder(self) -> EnforcementChangeDetectorBuilder:
        return EnforcementChangeDetectorBuilder()

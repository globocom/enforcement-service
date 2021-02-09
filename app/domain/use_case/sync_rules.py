import attr
from typing import List

from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.entities import ClusterRule, Cluster
from app.domain.source_locator import SourceLocator

from app.domain.use_case.responses import RulesResponse


@attr.s(auto_attribs=True)
class SyncRulesUseCase:
    _source_locator: SourceLocator
    _cluster_group_builder: ClusterGroupBuilder
    _enforcement_installer_builder: EnforcementInstallerBuilder

    def execute(self, cluster_rule: ClusterRule, current_clusters: List[Cluster]) -> RulesResponse:
        source_repository = self._source_locator.locate(cluster_rule.source)
        source_clusters = source_repository.get_clusters()

        source_cluster_group = self._cluster_group_builder.build(clusters=source_clusters)
        current_cluster_group = self._cluster_group_builder.build(clusters=current_clusters)

        deleted_clusters = current_cluster_group - source_cluster_group
        enforcement_uninstall = self._enforcement_installer_builder.build(
            cluster_group=deleted_clusters,
            enforcements=cluster_rule.enforcements
        )

        enforcement_uninstall.uninstall()
        deleted_clusters.unregister()

        new_clusters = source_cluster_group - current_cluster_group
        new_clusters.register()

        enforcement_installer = self._enforcement_installer_builder.build(
            cluster_group=new_clusters,
            enforcements=cluster_rule.enforcements
        )

        enforcement_installer.install()

        return RulesResponse(
            clusters=source_clusters,
        )




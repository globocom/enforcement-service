import attr

from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.entities import ClusterRule
from app.domain.source_locator import SourceLocator
from app.domain.use_case.responses import RulesResponse


@attr.s(auto_attribs=True)
class ApplyRulesUseCase:
    _source_locator: SourceLocator
    _cluster_group_builder: ClusterGroupBuilder
    _enforcement_installer_builder: EnforcementInstallerBuilder

    def execute(self, cluster_rule: ClusterRule) -> RulesResponse:
        source = self._source_locator.locate(cluster_rule.source)
        clusters = source.get_clusters()

        cluster_group = self._cluster_group_builder.build(clusters=clusters)
        cluster_group.register()

        enforcement_installer = self._enforcement_installer_builder.build(
            enforcements=cluster_rule.enforcements,
            cluster_group=cluster_group
        )

        enforcement_errors = enforcement_installer.install()
        response = RulesResponse(
            clusters=clusters,
            install_errors=enforcement_errors
        )

        return response


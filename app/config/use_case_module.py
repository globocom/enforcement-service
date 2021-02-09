from injector import Module, provider, singleton

from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_change_detector_builder import EnforcementChangeDetectorBuilder
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.repositories import EnforcementRepository
from app.domain.source_locator import SourceLocator
from app.domain.use_case import ApplyRulesUseCase, SyncRulesUseCase, UpdateRulesUseCase


class UseCaseModule(Module):

    @provider
    @singleton
    def provider_apply_rules(
            self, locator: SourceLocator,
            cluster_group_builder: ClusterGroupBuilder, enforcement_installer_builder: EnforcementInstallerBuilder
    ) -> ApplyRulesUseCase:
        return ApplyRulesUseCase(
            source_locator=locator,
            cluster_group_builder=cluster_group_builder,
            enforcement_installer_builder=enforcement_installer_builder
        )

    @provider
    @singleton
    def provider_sync_rules(
            self, locator: SourceLocator,
            cluster_group_builder: ClusterGroupBuilder, enforcement_installer_builder: EnforcementInstallerBuilder
    ) -> SyncRulesUseCase:
        return SyncRulesUseCase(
            cluster_group_builder=cluster_group_builder,
            source_locator=locator,
            enforcement_installer_builder=enforcement_installer_builder
        )

    @provider
    @singleton
    def provider_update_rules(self,
                              cluster_group_builder: ClusterGroupBuilder,
                              enforcement_installer_builder: EnforcementInstallerBuilder,
                              enforcement_change_detector_builder: EnforcementChangeDetectorBuilder) -> UpdateRulesUseCase:
        return UpdateRulesUseCase(
            cluster_group_builder=cluster_group_builder,
            enforcement_installer_builder=enforcement_installer_builder,
            enforcement_change_detector_builder=enforcement_change_detector_builder
        )

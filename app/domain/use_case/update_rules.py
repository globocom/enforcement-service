import attr
from typing import List

from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_change_detector import EnforcementChangeDetector
from app.domain.enforcement_change_detector_builder import EnforcementChangeDetectorBuilder
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.entities import Cluster, Enforcement

from app.domain.use_case.responses import UpdateRulesResponse


@attr.s(auto_attribs=True)
class UpdateRulesUseCase:
    _cluster_group_builder: ClusterGroupBuilder
    _enforcement_installer_builder: EnforcementInstallerBuilder
    _enforcement_change_detector_builder: EnforcementChangeDetectorBuilder

    def execute(self, clusters: List[Cluster], old_enforcements: List[Enforcement],
                new_enforcements: List[Enforcement]) -> UpdateRulesResponse:

        if not clusters:
            return UpdateRulesResponse()

        change_detector = self._enforcement_change_detector_builder.build(
            new_enforcements_list=new_enforcements,
            old_enforcements_list=old_enforcements
        )

        removed_enforcements = self._uninstall_removed_enforcements(change_detector, clusters)
        add_errors, install_enforcements = self._install_added_enforcements(change_detector, clusters)
        update_errors, update_enforcements = self._update_change_enforcements(change_detector, clusters)

        return UpdateRulesResponse(
            install_errors=add_errors + update_errors,
            added_enforcements=change_detector.detect_new_enforcements(),
            removed_enforcements=removed_enforcements,
            changed_enforcements=update_enforcements,
        )

    def _update_change_enforcements(self, change_detector: EnforcementChangeDetector,
                                    clusters: List[Cluster]) -> (List[Enforcement], List[Enforcement]):
        change_enforcements = change_detector.detect_change_enforcements()

        if not change_enforcements:
            return [], []

        cluster_group_change_enfocement = self._cluster_group_builder.build(
            clusters=clusters
        )

        enforcement_installer = self._enforcement_installer_builder.build(
            cluster_group=cluster_group_change_enfocement,
            enforcements=change_enforcements
        )

        return enforcement_installer.install(), change_enforcements

    def _install_added_enforcements(self, change_detector: EnforcementChangeDetector,
                                    clusters: List[Cluster]) -> (List[Enforcement], List[Enforcement]):
        added_enforcements = change_detector.detect_new_enforcements()

        if not added_enforcements:
            return [], []

        cluster_group_remove_enfocement = self._cluster_group_builder.build(
            clusters=clusters
        )

        enforcement_installer = self._enforcement_installer_builder.build(
            cluster_group=cluster_group_remove_enfocement,
            enforcements=added_enforcements
        )

        return enforcement_installer.install(), added_enforcements

    def _uninstall_removed_enforcements(self, change_detector: EnforcementChangeDetector,
                                        clusters: List[Cluster]) -> List[Enforcement]:

        removed_enforcements = change_detector.detect_removed_enforcements()

        if not removed_enforcements:
            return []

        cluster_group_remove_enfocement = self._cluster_group_builder.build(
            clusters=clusters
        )

        enforcement_installer = self._enforcement_installer_builder.build(
            cluster_group=cluster_group_remove_enfocement,
            enforcements=removed_enforcements
        )

        enforcement_installer.uninstall()

        return removed_enforcements


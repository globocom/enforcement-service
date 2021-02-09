from unittest import TestCase
from unittest.mock import MagicMock

from app.domain.cluster_group import ClusterGroup
from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_change_detector import EnforcementChangeDetector
from app.domain.enforcement_change_detector_builder import EnforcementChangeDetectorBuilder
from app.domain.enforcement_installer import EnforcementInstaller
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.entities import ClusterRule, Cluster, EnforcementSource, Enforcement
from app.domain.repositories import EnforcementRepository, ClusterRepository, ProjectRepository
from app.domain.use_case import UpdateRulesUseCase


class UpdateRulesTestCase(TestCase):
    def setUp(self) -> None:
        self.cluster_repository = ClusterRepository()
        self.project_repository = ProjectRepository()
        self.enforcement_repository = EnforcementRepository()
        self.enforcement = Enforcement(name='test', repo='somewhere')
        self.old_enforcement = Enforcement(name='test', repo='somewhere')
        self.new_enforcement = Enforcement(name='test1', repo='anywhere')
        self.cluster = Cluster(name='test', url='test',
                               token='test', id='test')
        self.cluster_group = ClusterGroup(clusters=[self.cluster],
                                          cluster_repository=self.cluster_repository,
                                          project_repository=self.project_repository
                                          )

        self.cluster_group_builder = ClusterGroupBuilder(
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )

        self.cluster_rule = ClusterRule(
            enforcements=[self.enforcement], source=EnforcementSource())

        self.enforcement_installer_builder = EnforcementInstallerBuilder(
            enforcement_repository=self.enforcement_repository
        )

        self.enforcement_installer = EnforcementInstaller(
            enforcements=[self.enforcement],
            cluster_group=self.cluster_group,
            enforcement_repository=self.enforcement_repository
        )

        self.enforcement_change_detector_builder = EnforcementChangeDetectorBuilder()
        self.enforcement_change_detector = EnforcementChangeDetector(
            old_enforcements_list=[self.old_enforcement],
            new_enforcements_list=[self.new_enforcement]
        )

    def test_execute(self) -> None:
        self.enforcement_change_detector_builder.build = MagicMock(
            return_value=self.enforcement_change_detector)
        self.cluster_group_builder.build = MagicMock(
            return_value=self.cluster_group)
        self.enforcement_installer_builder.build = MagicMock(
            return_value=self.enforcement_installer)
        self.enforcement_installer.uninstall = MagicMock(retun_value=None)
        self.enforcement_installer.install = MagicMock(retun_value=None)

        update_rules_use_case = UpdateRulesUseCase(
            cluster_group_builder=self.cluster_group_builder,
            enforcement_installer_builder=self.enforcement_installer_builder,
            enforcement_change_detector_builder=self.enforcement_change_detector_builder
        )

        response = update_rules_use_case.execute(
            clusters=[self.cluster],
            old_enforcements=[self.old_enforcement],
            new_enforcements=[self.new_enforcement]
        )

        self.assertEqual(0, len(response.clusters))
        self.assertEqual(0, len(response.install_errors))
        self.assertTrue(self.enforcement_change_detector_builder.build.called)
        self.assertTrue(self.cluster_group_builder.build.called)
        self.assertTrue(self.enforcement_installer_builder.build.called)
        self.assertTrue(self.enforcement_installer.uninstall.called)
        self.assertTrue(self.enforcement_installer.install.called)
            

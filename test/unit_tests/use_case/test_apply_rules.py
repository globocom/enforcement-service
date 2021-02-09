from typing import List
from unittest import TestCase
from unittest.mock import MagicMock

from app.domain.cluster_group import ClusterGroup
from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_installer import EnforcementInstaller
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.entities import ClusterRule, Cluster, EnforcementSource, Enforcement
from app.domain.repositories import EnforcementRepository, ClusterRepository, ProjectRepository, SourceRepository
from app.domain.source_locator import SourceLocator
from app.domain.use_case import ApplyRulesUseCase


class ApplyRulesTestCase(TestCase):
    def setUp(self) -> None:
        self.source_locator = SourceLocator()
        self.source_repository = SourceRepository()
        self.cluster_repository = ClusterRepository()
        self.project_repository = ProjectRepository()
        self.enforcement_repository = EnforcementRepository()
        self.enforcement = Enforcement(name='test', repo='somewhere')

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
            enforcements=[], source=EnforcementSource())

        self.enforcement_installer_builder = EnforcementInstallerBuilder(
            enforcement_repository=self.enforcement_repository
        )
        self.enforcement_installer = EnforcementInstaller(
            enforcements=[self.enforcement],
            cluster_group=self.cluster_group,
            enforcement_repository=self.enforcement_repository
        )

    def test_execute(self) -> None:
        self.source_locator.locate = MagicMock(
            return_value=self.source_repository)
        self.source_repository.get_clusters = MagicMock(
            return_value=[self.cluster])
        self.cluster_group_builder.build = MagicMock(
            return_value=self.cluster_group)
        self.cluster_group.register = MagicMock(return_value=None)
        self.enforcement_installer_builder.build = MagicMock(
            return_value=self.enforcement_installer)
        self.enforcement_installer.install = MagicMock(retun_value=None)

        apply_rules = ApplyRulesUseCase(
            source_locator=self.source_locator,
            cluster_group_builder=self.cluster_group_builder,
            enforcement_installer_builder=self.enforcement_installer_builder
        )

        response = apply_rules.execute(self.cluster_rule)

        self.assertEqual(1, len(response.clusters))
        self.assertEqual(0, len(response.install_errors))
        self.assertTrue(self.source_locator.locate.called)
        self.assertTrue(self.source_repository.get_clusters.called)
        self.assertTrue(self.cluster_group_builder.build.called)
        self.assertTrue(self.cluster_group.register.called)
        self.assertTrue(self.enforcement_installer_builder.build.called)
        self.assertTrue(self.enforcement_installer.install.called)

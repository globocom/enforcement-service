from unittest import TestCase

from app.domain.cluster_group import ClusterGroup
from app.domain.enforcement_installer import EnforcementInstaller
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.entities import Enforcement, Cluster
from app.domain.repositories import EnforcementRepository, ClusterRepository, ProjectRepository


class EnforcementInstallerBuilderTestCase(TestCase):
    def setUp(self) -> None:
        self.enforcement_repository = EnforcementRepository()
        self.enforcement = Enforcement(name='test', repo='somewhere')
        self.cluster_repository = ClusterRepository()
        self.project_repository = ProjectRepository()
        self.cluster = Cluster(name='test', url='test',
                               token='test', id='test')
        self.cluster_group = ClusterGroup(
            clusters=[self.cluster],
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )
        self.enforcement_installer = EnforcementInstaller(
            enforcements=[self.enforcement],
            cluster_group=self.cluster_group,
            enforcement_repository=self.enforcement_repository
        )

    def test_build(self) -> None:
        enforcement_installer_builder = EnforcementInstallerBuilder(
            enforcement_repository=self.enforcement_repository
        )

        enforcement_installer = enforcement_installer_builder.build(
            enforcements=[self.enforcement],
            cluster_group=self.cluster_group
        )

        self.assertEqual(self.enforcement_installer, enforcement_installer)

    def test_build_throws_exception_required_argument(self) -> None:
        enforcement_installer_builder = EnforcementInstallerBuilder(
            enforcement_repository=self.enforcement_repository
        )
        
        with self.assertRaises(Exception) as context:
            enforcement_installer_builder.build()

        self.assertTrue('required positional argument' in str(context.exception))
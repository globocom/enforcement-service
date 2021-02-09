from unittest import TestCase

from app.domain.cluster_group import ClusterGroup
from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.entities import Cluster
from app.domain.repositories import ClusterRepository, ProjectRepository


class ClusterGroupBuilderTestCase(TestCase):
    def setUp(self) -> None:
        self.cluster_repository = ClusterRepository()
        self.project_repository = ProjectRepository()
        self.cluster = Cluster(name='test', url='test',
                               token='test', id='test')
        self.cluster_group = ClusterGroup(
            clusters=[self.cluster],
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )

    def test_build(self) -> None:
        cluster_group_builder = ClusterGroupBuilder(
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )

        cluster_group = cluster_group_builder.build([
            self.cluster
        ])

        self.assertEqual(self.cluster_group, cluster_group)


    def test_build_throws_exception_required_argument(self) -> None:
        cluster_group_builder = ClusterGroupBuilder(
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )

        with self.assertRaises(Exception) as context:
            cluster_group_builder.build()

        self.assertTrue('required positional argument' in str(context.exception))
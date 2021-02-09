from unittest import TestCase
from unittest.mock import patch

from app.domain.cluster_group import ClusterGroup
from app.domain.entities import Cluster
from app.domain.repositories import ClusterRepository, ProjectRepository


class ClusterGroupTestCase(TestCase):
    def setUp(self) -> None:
        self.cluster_repository = ClusterRepository()
        self.project_repository = ProjectRepository()
        self.cluster = Cluster(name='test', url='test',
                               token='test', id='test')

    @patch('app.domain.repositories.ProjectRepository.create_project')
    @patch('app.domain.repositories.ClusterRepository.register_cluster')
    def test_register(self, mock_register_cluster, mock_create_project) -> None:
        cluster_group = ClusterGroup(
            clusters=[self.cluster],
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )

        cluster_group.register()

        self.assertTrue(mock_register_cluster.called)
        self.assertEqual(mock_register_cluster.call_args[0][0], self.cluster)
        self.assertTrue(mock_create_project.called)
        self.assertEqual(mock_create_project.call_args[0][0], self.cluster)

    @patch('app.domain.repositories.ProjectRepository.remove_project')
    @patch('app.domain.repositories.ClusterRepository.unregister_cluster')
    def test_unregister(self, mock_unregister_cluster, mock_remove_project) -> None:
        cluster_group = ClusterGroup(
            clusters=[self.cluster],
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )

        cluster_group.unregister()

        self.assertTrue(mock_unregister_cluster.called)
        self.assertEqual(
            mock_unregister_cluster.call_args[0][0], self.cluster)
        self.assertTrue(mock_remove_project.called)
        self.assertEqual(mock_remove_project.call_args[0][0], self.cluster.name)

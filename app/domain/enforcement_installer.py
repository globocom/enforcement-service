from typing import List

import attr

from app.domain.cluster_group import ClusterGroup
from app.domain.entities import Enforcement, Cluster
from app.domain.repositories import EnforcementRepository
from app.domain.exceptions import EnforcementInvalidException


@attr.s(auto_attribs=True)
class EnforcementInstaller:
    _enforcements: List[Enforcement]
    _cluster_group: ClusterGroup
    _enforcement_repository: EnforcementRepository

    def install(self) -> List[Enforcement]:

        enforcements_error: List[Enforcement] = []

        for cluster in self._cluster_group.clusters:
            installed_enforcements = self._enforcement_repository.list_installed_enforcements(cluster_name=cluster.name)
            installed_enforcements_names = self._get_enforcements_name(installed_enforcements)
            for enforcement in self._enforcements:
                instance_name = self._make_enforcement_name(cluster, enforcement)
                try:
                    if instance_name not in installed_enforcements_names:
                        self._enforcement_repository.create_enforcement(cluster.name, instance_name, enforcement)
                    else:
                        self._enforcement_repository.update_enforcement(cluster.name, instance_name, enforcement)
                except EnforcementInvalidException:
                    enforcements_error.append(enforcement)

        return enforcements_error

    def uninstall(self):
        for cluster in self._cluster_group.clusters:
            installed_enforcements = self._enforcement_repository.list_installed_enforcements(cluster_name=cluster.name)
            installed_enforcements_names = self._get_enforcements_name(installed_enforcements)
            for enforcement in self._enforcements:
                instance_name = self._make_enforcement_name(cluster, enforcement)
                if instance_name in installed_enforcements_names:
                    self._enforcement_repository.remove_enforcement(instance_name)

    @classmethod
    def _get_enforcements_name(cls, enforcements: List[Enforcement]):
        return {enforcement.name: enforcement for enforcement in enforcements}

    @classmethod
    def _make_enforcement_name(cls, cluster: Cluster, enforcement: Enforcement) -> str:
        return f"{cluster.name}-{enforcement.name}"

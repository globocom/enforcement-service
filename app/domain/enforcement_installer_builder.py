from typing import List

import attr

from app.domain.cluster_group import ClusterGroup
from app.domain.enforcement_installer import EnforcementInstaller
from app.domain.entities import Enforcement
from app.domain.repositories import EnforcementRepository


@attr.s(auto_attribs=True)
class EnforcementInstallerBuilder:
    _enforcement_repository: EnforcementRepository

    def build(self, enforcements: List[Enforcement], cluster_group: ClusterGroup) -> EnforcementInstaller:
        return EnforcementInstaller(
            enforcements=enforcements,
            cluster_group=cluster_group,
            enforcement_repository=self._enforcement_repository
        )

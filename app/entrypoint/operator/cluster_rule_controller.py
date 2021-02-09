from typing import ClassVar, List

import attr
import kopf
from injector import inject

from app.entrypoint.operator.base_controller import BaseController
from app.domain.entities import ClusterRule, ClusterRuleStatus, Cluster, Enforcement
from app.domain.use_case import ApplyRulesUseCase, SyncRulesUseCase, UpdateRulesUseCase, RulesResponse


@inject
@attr.s(auto_attribs=True)
class ClusterRuleController(BaseController):
    _apply_rules_use_case: ApplyRulesUseCase
    _sync_rules_use_case: SyncRulesUseCase
    _update_rules_use_case: UpdateRulesUseCase
    KIND: ClassVar[str] = 'clusterrules'
    ID: ClassVar[str] = "sync/spec.enforcements"
    BACKOFF: ClassVar[int] = 10
    SYNC_INTERVAL: ClassVar[int] = 6
    SYNC_INITIAL_DELAY: ClassVar[int] = 20
    SYNC_IDLE: ClassVar[int] = 15

    def update(self, name, old: List[dict], new: List[dict], status: dict, logger, **kwargs):
        if not old:
            return

        logger.debug(f"update rules for %s", name)

        old_enforcement_list = ClusterRuleController._make_enforcement_list(old)
        new_enforcement_list = ClusterRuleController._make_enforcement_list(new)
        current_status = ClusterRuleController._restore_status(status)

        current_clusters = [
            Cluster(name=cluster['name'], url=cluster['url'], id='', token='')
            for cluster in current_status.clusters
        ]

        response = self._update_rules_use_case.execute(
            clusters=current_clusters,
            old_enforcements=old_enforcement_list,
            new_enforcements=new_enforcement_list,
        )

        enforcements_change = [
            enforcement.name for enforcement in response.removed_enforcements + response.changed_enforcements
        ]

        response.install_errors = response.install_errors + list(
            map(
                lambda name: Enforcement(name=name, repo=""),
                filter(
                    lambda enforcement_name: enforcement_name not in enforcements_change,
                    current_status.install_errors,
                )
            )
        )

        response.clusters = current_clusters

        return ClusterRuleController._make_status(response)

    def sync(self, name: str, spec: dict, status: dict, logger, **kwargs):
        logger.debug(f"sync clusters for %s", name)

        current_status = ClusterRuleController._restore_status(status)

        if not current_status:
            return

        current_clusters = [
            Cluster(name=cluster['name'], url=cluster['url'], id='', token='')
            for cluster in current_status.clusters
        ]
        cluster_rule = ClusterRule(**spec)

        response = self._sync_rules_use_case.execute(cluster_rule, current_clusters)
        response.install_errors = [Enforcement(name=name, repo="") for name in current_status.install_errors]

        new_status = ClusterRuleController._make_status(response)

        if new_status != current_status.dict():
            return new_status

    def create(self, name, spec: dict, logger, **kwargs):
        logger.debug(f"create rules for %s", name)

        cluster_rule = ClusterRule(**spec)

        response = self._apply_rules_use_case.execute(cluster_rule)

        return ClusterRuleController._make_status(response)

    def register(self):

        self.register_method(kopf.on.create, self.create, self.KIND, id=ClusterRuleController.ID,
                             errors=kopf.ErrorsMode.TEMPORARY, backoff=ClusterRuleController.BACKOFF)

        self.register_method(kopf.on.field, self.update, self.KIND, id='sync',
                             field='spec.enforcements', errors=kopf.ErrorsMode.TEMPORARY,
                             backoff=ClusterRuleController.BACKOFF)

        self.register_method(kopf.on.timer, self.sync, self.KIND, id=ClusterRuleController.ID,
                             interval=6, initial_delay=20, idle=15, errors=kopf.ErrorsMode.PERMANENT)

    @classmethod
    def _make_enforcement_list(cls, enforcement_map_list) -> List[Enforcement]:
        if not enforcement_map_list:
            return []
        return [Enforcement(**enforcement_map) for enforcement_map in enforcement_map_list]

    @classmethod
    def _make_status(cls, response: RulesResponse) -> dict:
        status = ClusterRuleStatus(
            install_errors=[
                enforcement.name for enforcement in response.install_errors
            ],
            clusters=[
                {"name": cluster.name, "url": cluster.url} for cluster in response.clusters
            ]
        )
        return status.dict()

    @classmethod
    def _restore_status(cls, status: dict) -> ClusterRuleStatus:
        current_status: dict = status.get(ClusterRuleController.ID)

        return ClusterRuleStatus(**current_status) \
            if current_status and current_status.get("clusters") else None

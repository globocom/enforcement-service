from typing import Dict, List, Any

import attr
from argocd_client import (
    V1alpha1ApplicationDestination,
    V1alpha1Application,
    V1alpha1ApplicationSpec,
    ApplicationServiceApi,
    V1ObjectMeta,
    V1alpha1SyncPolicy,
    V1alpha1SyncPolicyAutomated,
    V1alpha1ApplicationList,
    V1alpha1ApplicationSource,
    V1alpha1ApplicationSourceHelm,
    V1alpha1HelmParameter,
    ApiException
)

from app.domain.entities import Enforcement, Helm
from app.domain.repositories import EnforcementRepository
from app.domain.exceptions import EnforcementInvalidException
from app.infra.logger import logger


@attr.s(auto_attribs=True)
class ApplicationService(EnforcementRepository):
    _application_service: ApplicationServiceApi

    def create_enforcement(self, cluster_name: str, instance_name: str, enforcement: Enforcement) -> None:
        application = self._make_application_by_enforcement(cluster_name, instance_name, enforcement)

        try:
            self._application_service.create_mixin9(application)
        except ApiException as e:
            if e.status == 400:
                raise EnforcementInvalidException(e.__str__())
            raise e

    def update_enforcement(self, cluster_name: str, instance_name: str, enforcement: Enforcement) -> None:
        application = self._make_application_by_enforcement(cluster_name, instance_name, enforcement)

        try:
            self._application_service.update_mixin9(application.metadata.name, application)
        except ApiException as e:
            if e.status == 400:
                raise EnforcementInvalidException(e.__str__())
            raise e

    def remove_enforcement(self, enforcement_name: str) -> None:
        application = V1alpha1Application(
            metadata=V1ObjectMeta(
                name=enforcement_name
            )
        )

        self._application_service.delete_mixin9(application.metadata.name, cascade=False)
        logger.info(f"Application {application.metadata.name} removed")

    def list_installed_enforcements(self, **filters: Any) -> List[Enforcement]:
        labels = self._make_labels(filters)
        application_list: V1alpha1ApplicationList = self._application_service.list_mixin9(
            selector=labels
        )

        applications: List[V1alpha1Application] = application_list.items if application_list.items else []

        enforcements = [
            self._make_enforcement_by_application(application)
            for application in applications
        ]

        return enforcements

    def _make_labels(self, labels: Dict[str, str]) -> str:
        list_labels = [f"{key}={value}" for key, value in list(labels.items())]
        separator = ","
        return separator.join(list_labels)

    def _make_application_by_enforcement(self, cluster_name: str, instance_name: str,
                                         enforcement: Enforcement) -> V1alpha1Application:
        source = V1alpha1ApplicationSource(path=enforcement.path, repo_url=enforcement.repo)

        if enforcement.helm:
            source.helm = V1alpha1ApplicationSourceHelm(
                parameters=[
                    V1alpha1HelmParameter(
                        name=key,
                        value=value
                    )
                    for key, value in enforcement.helm.parameters.items()
                ] if enforcement.helm.parameters else []
            )

        return V1alpha1Application(
            metadata=V1ObjectMeta(
                name=f"{instance_name}",
                labels={"cluster_name": cluster_name},
            ),
            spec=V1alpha1ApplicationSpec(
                destination=V1alpha1ApplicationDestination(
                    name=cluster_name,
                    namespace=enforcement.namespace
                ),
                source=source,
                sync_policy=V1alpha1SyncPolicy(
                    automated=V1alpha1SyncPolicyAutomated(
                        prune=True,
                        self_heal=True,
                    )
                )
            )
        )

    def _make_enforcement_by_application(self, application: V1alpha1Application) -> Enforcement:

        helm_source: V1alpha1ApplicationSourceHelm = application.spec.source.helm
        helm = None

        if helm_source and helm_source.parameters:
            helm_params = {param.name: param.value for param in helm_source.parameters}
            helm = Helm(parameters=helm_params)

        return Enforcement(
            name=application.metadata.name,
            repo=application.spec.source.repo_url,
            path=application.spec.source.path,
            helm=helm
        )

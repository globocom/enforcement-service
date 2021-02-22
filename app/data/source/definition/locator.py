from app.data.source.definition.register import SourceRegister
from app.domain.entities import EnforcementSource
from app.domain.repositories import SourceRepository
from app.domain.source_locator import SourceLocator
from app.infra.config import Config
from app.infra.kubernetes_helper import KubernetesHelper


class SourceLocatorImpl(SourceLocator):

    def __init__(self, config_helper: Config, kubernetes_helper: KubernetesHelper):
        self._config_helper = config_helper
        self._kubernetes_helper = kubernetes_helper

    def locate(self, source: EnforcementSource) -> SourceRepository:
        source_name = [key for key, value in source.__dict__.items() if value is not None][0]
        datasource_class = SourceRegister.find_source(source_name)

        if not datasource_class:
            raise Exception("Source not defined")

        return datasource_class(config=self._config_helper, source=source, kubernetes_helper=self._kubernetes_helper,
                                secret=None, source_name=source_name)

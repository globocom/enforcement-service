from app.domain.entities import EnforcementSource
from app.domain.repositories import SourceRepository


class SourceLocator:
    def locate(self, source: EnforcementSource) -> SourceRepository:
        pass
from dataclasses import dataclass, field
from typing import List
from app.domain.entities import Cluster, Enforcement


@dataclass
class RulesResponse:
    clusters: List[Cluster] = field(default_factory=list)
    install_errors: List[Enforcement] = field(default_factory=list)


@dataclass
class UpdateRulesResponse(RulesResponse):
    removed_enforcements: List[Enforcement] = field(default_factory=list)
    changed_enforcements: List[Enforcement] = field(default_factory=list)
    added_enforcements: List[Enforcement] = field(default_factory=list)


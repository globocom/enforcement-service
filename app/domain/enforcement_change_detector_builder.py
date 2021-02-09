from typing import List

from app.domain.enforcement_change_detector import EnforcementChangeDetector
from app.domain.entities import Enforcement


class EnforcementChangeDetectorBuilder:
    def build(self, new_enforcements_list: List[Enforcement],
              old_enforcements_list: List[Enforcement]) -> EnforcementChangeDetector:
        return EnforcementChangeDetector(new_enforcements_list=new_enforcements_list,
                                         old_enforcements_list=old_enforcements_list)

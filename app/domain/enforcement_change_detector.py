from typing import List, Dict

import attr

from app.domain.entities import Enforcement


@attr.s(auto_attribs=True)
class EnforcementChangeDetector:
    _new_enforcements_list: List[Enforcement]
    _old_enforcements_list: List[Enforcement]

    def __attrs_post_init__(self):
        self._new_enforcements_map = self._new_enforcement_map(self._new_enforcements_list)
        self._old_enforcements_map = self._new_enforcement_map(self._old_enforcements_list)

    def detect_new_enforcements(self) -> List[Enforcement]:
        return self._diff_enforcements_map(
            self._new_enforcements_map, self._old_enforcements_map
        )

    def detect_removed_enforcements(self) -> List[Enforcement]:
        return self._diff_enforcements_map(
            self._old_enforcements_map,
            self._new_enforcements_map
        )

    def detect_change_enforcements(self) -> List[Enforcement]:
        def compare(new_enforcement: Enforcement) -> bool:
            old_enforcement = self._old_enforcements_map.get(new_enforcement.name)
            if not old_enforcement:
                return False

            return new_enforcement != old_enforcement

        return list(
            filter(
                compare,
                self._new_enforcements_list
            )
        )

    @classmethod
    def _diff_enforcements_map(cls, dict1: Dict[str, Enforcement], dict2: Dict[str, Enforcement]) -> List[Enforcement]:
        diff_enforcement_names = set(dict1.keys()) \
            .difference(set(dict2.keys()))

        diff_enforcements = [
            dict1[name] for name in diff_enforcement_names
        ]

        return diff_enforcements

    @classmethod
    def _new_enforcement_map(cls, enforcements: List[Enforcement]) -> Dict[str, Enforcement]:
        return {enforcement.name: enforcement for enforcement in enforcements}

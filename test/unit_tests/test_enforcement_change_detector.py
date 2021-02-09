from unittest import TestCase
from unittest.mock import patch
from app.domain.enforcement_change_detector import EnforcementChangeDetector
from app.domain.entities import Enforcement


class EnforcementChangeDetectorTestCase(TestCase):
    def test_detect_new_enforcements(self) -> None:
        new_enforcement = [Enforcement(name='git', repo='somewhere')]
        old_enforcement = [Enforcement(name='hub', repo='anywhere')]
        enforcement_change_detector = EnforcementChangeDetector(
            new_enforcements_list=new_enforcement,
            old_enforcements_list=old_enforcement
        )

        enforcements = enforcement_change_detector.detect_new_enforcements()
        self.assertEqual(new_enforcement, enforcements)

    def test_detect_new_enforcements_with_no_changes(self) -> None:
        new_enforcement = [Enforcement(name='hub', repo='anywhere')]
        old_enforcement = [Enforcement(name='hub', repo='anywhere')]

        enforcement_change_detector = EnforcementChangeDetector(
            new_enforcements_list=new_enforcement,
            old_enforcements_list=old_enforcement
        )

        enforcements = enforcement_change_detector.detect_new_enforcements()
        self.assertEqual([], enforcements)

    def test_detect_removed_enforcements(self) -> None:
        new_enforcement = [Enforcement(name='hub', repo='anywhere')]
        old_enforcement = [Enforcement(name='git', repo='anywhere')]

        enforcement_change_detector = EnforcementChangeDetector(
            new_enforcements_list=new_enforcement,
            old_enforcements_list=old_enforcement
        )
        enforcements = enforcement_change_detector.detect_removed_enforcements()
        self.assertEqual(old_enforcement, enforcements)

    def test_detect_removed_enforcements_with_no_changes(self) -> None:
        new_enforcement = [Enforcement(name='git', repo='anywhere')]
        old_enforcement = [Enforcement(name='git', repo='anywhere')]

        enforcement_change_detector = EnforcementChangeDetector(
            new_enforcements_list=new_enforcement,
            old_enforcements_list=old_enforcement
        )
        enforcements = enforcement_change_detector.detect_removed_enforcements()
        self.assertEqual([], enforcements)

    def test_detect_change_enforcements(self) -> None:
        new_enforcement = [Enforcement(name='hub', repo='anywhere')]
        old_enforcement = [Enforcement(name='hub', repo='test')]

        enforcement_change_detector = EnforcementChangeDetector(
            new_enforcements_list=new_enforcement,
            old_enforcements_list=old_enforcement
        )

        enforcements = enforcement_change_detector.detect_change_enforcements()
        self.assertEqual(new_enforcement, enforcements)
    

    def test_detect_change_enforcements_with_no_changes(self) -> None:
        new_enforcement = [Enforcement(name='hub', repo='anywhere')]
        old_enforcement = [Enforcement(name='hub', repo='anywhere')]

        enforcement_change_detector = EnforcementChangeDetector(
            new_enforcements_list=new_enforcement,
            old_enforcements_list=old_enforcement
        )
        enforcements = enforcement_change_detector.detect_change_enforcements()
        self.assertEqual([], enforcements)
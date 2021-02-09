from unittest import TestCase

from app.domain.enforcement_change_detector import EnforcementChangeDetector
from app.domain.enforcement_change_detector_builder import EnforcementChangeDetectorBuilder
from app.domain.entities import Enforcement


class EnforcementChangeDetectorBuilderTestCase(TestCase):
    def setUp(self) -> None:
        self.enforcement = Enforcement(name='test', repo='somewhere')
        self.enforcement_installer = EnforcementChangeDetector(
            new_enforcements_list=[self.enforcement],
            old_enforcements_list=[self.enforcement],
        )

    def test_build(self) -> None:
        enforcement_change_detector_builder = EnforcementChangeDetectorBuilder()
        enforcement_change_detector = enforcement_change_detector_builder.build(
            old_enforcements_list=[self.enforcement],
            new_enforcements_list=[self.enforcement])
        self.assertEqual(self.enforcement_installer,
                         enforcement_change_detector)

    def test_build_throws_exception_required_argument(self) -> None:
        enforcement_change_detector_builder = EnforcementChangeDetectorBuilder()
        
        with self.assertRaises(Exception) as context:
            enforcement_change_detector_builder.build()

        self.assertTrue('required positional argument' in str(context.exception))
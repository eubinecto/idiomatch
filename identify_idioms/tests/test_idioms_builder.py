from typing import Optional, List
from unittest import TestCase
from identify_idioms.builders import IdiomsBuilder


class TestIdiomsBuilder(TestCase):
    idioms_builder: Optional[IdiomsBuilder] = None
    idioms: Optional[List[str]] = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.idioms_builder = IdiomsBuilder()
        cls.idioms = cls.idioms_builder.construct()

    def test_hyphenated_term_included_catch_22(self):
        self.assertIn("catch-22", self.idioms)

    def test_hyphenated_term_included_balls_out(self):
        self.assertIn("balls-out", self.idioms)

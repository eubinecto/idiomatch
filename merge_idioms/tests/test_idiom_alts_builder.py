from typing import Optional, List, Dict
from unittest import TestCase
from builders import IdiomAltsBuilder
from config import SLIDE_IDIOM_ALTS_TSV


class TestIdiomAltsScraper(TestCase):
    idiom_alts_builder: Optional[IdiomAltsBuilder] = None
    idiom_alts: Optional[Dict[str, List]] = None
    idioms: Optional[List[str]] = None
    alts: Optional[List[str]] = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.idiom_alts_builder = IdiomAltsBuilder()
        cls.idiom_alts = cls.idiom_alts_builder.construct(SLIDE_IDIOM_ALTS_TSV)
        cls.idioms = [
            idiom
            for idiom, _ in cls.idiom_alts.items()
        ]
        cls.alts = [
            alt
            for _, alts in cls.idiom_alts.items()
            for alt in alts
        ]

    def test_hyphenated_term_included_catch_22(self):
        self.assertIn("catch-22", self.idioms)

    def test_hyphenated_term_included_balls_out(self):
        self.assertIn("balls-out", self.idioms)

    def test_alts_included_have_blood_on_ones_hands(self):
        self.assertIn("have one's blood on one's hands", self.alts)


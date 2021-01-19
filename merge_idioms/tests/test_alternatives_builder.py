from typing import Optional
from unittest import TestCase
from builders import AlternativesBuilder


class TestAlternativesBuilder(TestCase):
    alts_builder: Optional[AlternativesBuilder] = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.alts_builder = AlternativesBuilder()

    def test_when_alternatives_exist(self):
        idiom_lemma = "beat around the bush"
        self.alts_builder.construct(lemma=idiom_lemma)
        self.assertIn("beat about the bush", self.alts_builder.alternatives)

    def test_when_alternatives_do_not_exist(self):
        # should be an empty list
        idiom_lemma = "go for it"
        self.alts_builder.construct(lemma=idiom_lemma)
        self.assertFalse(self.alts_builder.alternatives)

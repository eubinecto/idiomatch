from typing import Optional
from unittest import TestCase
from builders import AlternativesBuilder


class TestAlternativesBuilder(TestCase):
    alts_builder: Optional[AlternativesBuilder] = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.alts_builder = AlternativesBuilder()

    def test_when_alts_exist_beat_around_the_bush(self):
        idiom_lemma = "beat around the bush"
        self.alts_builder.construct(lemma=idiom_lemma)
        self.assertIn("beat about the bush", self.alts_builder.alts)

    def test_when_alts_exist_catch_em_up(self):
        idiom_lemma = "shoot 'em up"
        alts = "shoot-em-up,shoot-'em-up,shoot them up"
        self.alts_builder.construct(lemma=idiom_lemma)
        for alt in alts.split(","):
            self.assertIn(alt, self.alts_builder.alts)

    def test_when_alts_do_not_exist_empty_list_go_for_it(self):
        # should be an empty list
        idiom_lemma = "go for it"
        self.alts_builder.construct(lemma=idiom_lemma)
        # must be an empty list
        self.assertIsInstance(self.alts_builder.alts, list)
        self.assertFalse(self.alts_builder.alts)

    # note that the lemma must be as-is in wiktionary. Don't use the normalised form.
    def test_when_alts_do_not_exist_empty_list_elysian_fields_capitalised(self):
        idiom_lemma = "Elysian Fields"
        self.alts_builder.construct(lemma=idiom_lemma)
        # must be an empty list
        self.assertIsInstance(self.alts_builder.alts, list)
        self.assertFalse(self.alts_builder.alts)
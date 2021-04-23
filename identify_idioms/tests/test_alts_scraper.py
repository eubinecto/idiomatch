from typing import Optional
from unittest import TestCase
from identify_idioms.scrapers import AltsScraper


class TestAltsScraper(TestCase):
    alts_scraper: Optional[AltsScraper] = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.alts_scraper = AltsScraper()

    def test_when_alts_exist_beat_around_the_bush(self):
        idiom = "beat around the bush"
        alt = "beat about the bush"
        alts = self.alts_scraper.fetch(idiom)
        self.assertIn(alt, alts)
        self.assertTrue(len(alts) == 1)

    def test_when_alts_exist_catch_em_up(self):
        idiom = "shoot 'em up"
        alts = self.alts_scraper.fetch(idiom)
        for alt in "shoot-em-up,shoot-'em-up,shoot them up".split(","):
            self.assertIn(alt, alts)
        self.assertTrue(len(alts) == 3)

    # thankfully, they are stated in wiktionary.
    def test_when_alts_exist_piece_de_resistance(self):
        idiom = "pièce de résistance"
        alt = "piece de resistance"
        alts = self.alts_scraper.fetch(idiom)
        self.assertIn(alt, alts)
        self.assertTrue(len(alts) == 1)

    def test_when_alts_exist_creme_de_la_creme(self):
        idiom = "crème de la crème"
        alt = "creme de la creme"
        alts = self.alts_scraper.fetch(idiom)
        self.assertIn(alt, alts)
        self.assertTrue(len(alts) == 1)

    def test_when_alts_exist_wet_behind_the_ears(self):
        idiom = "wet behind the ears"
        alts = self.alts_scraper.fetch(idiom)
        for alt in "green behind the ears,wet-behind-the-ears".split(","):
            self.assertIn(alt, alts)
        self.assertTrue(len(alts) == 2)

    def test_when_alts_do_not_exist_empty_list_go_for_it(self):
        # should be an empty list
        idiom = "go for it"
        alts = self.alts_scraper.fetch(idiom)
        # must be an empty list
        self.assertIsInstance(alts, list)
        self.assertFalse(alts)

    # note that the lemma must be as-is in wiktionary. Don't use the normalised form.
    def test_when_alts_do_not_exist_empty_list_elysian_fields_capitalised(self):
        idiom = "Elysian Fields"
        alts = self.alts_scraper.fetch(idiom)
        # must be an empty list
        self.assertIsInstance(alts, list)
        self.assertFalse(alts)

from typing import List, Optional
from unittest import TestCase
from builders import MIPBuilder
from spacy import Language


class TestMergeIdiomsPipeline(TestCase):
    # merge-idioms-pipeline.
    # to be used globally.
    mip: Optional[Language] = None

    # utils.
    @classmethod
    def get_lemmas(cls, sent: str) -> List[str]:
        """
        returns a string representation of the lemma
        """
        doc = cls.mip(sent)
        return [
            token.lemma_
            for token in doc
        ]

    @classmethod
    def get_lemma_ids(cls, sent: str) -> List[int]:
        """
        returns a hash code for the lemma. I call this "lemma_id".
        this is the one that vocab.strings receives.
        """
        doc = cls.mip(sent)
        return [
            token.lemma
            for token in doc
        ]

    @classmethod
    def setUpClass(cls):
        """
        https://stackoverflow.com/a/12202239
        """
        # prepare resource, before running any tests below
        # I get some rsrc-related warning. Not sure why.
        mip_builder = MIPBuilder()
        mip_builder.construct()
        cls.mip = mip_builder.mip

    def test_greedily_normalize_on_ones_hands(self):
        sent_1 = "I've got too much on my hands to help."
        sent_2 = "If she dies, her blood is on your hands!"  # does not include "have"
        # this is more close to have one's blood on one's hands.
        # but simply impossible to catch that with hard-coded rules
        sent_3 = "The leaders of this war have the blood of many thousands of people on their hands."

        lemmas_1 = self.get_lemmas(sent_1)
        lemmas_2 = self.get_lemmas(sent_2)
        lemmas_3 = self.get_lemmas(sent_3)
        self.assertIn("on one's hands", lemmas_1)
        self.assertIn("on one's hands", lemmas_2)
        self.assertIn("on one's hands", lemmas_3)

    def test_greedily_normalize_have_ones_blood_on_ones_hands(self):
        sent_1 = "If she dies, you have her blood on your hands!"
        # later... you have to test for this. should include the case of having the in place of one's
        # sent_1 = "If she dies, you have the blood on your hands!"
        lemmas_1 = self.get_lemmas(sent_1)
        # so, the problem is, this fails.
        self.assertIn("have one's blood on one's hands", lemmas_1)

    def test_greedily_normalize_line_in_the_sand(self):
        sent_1 = "Your line in the sand is not so absolute."
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("line in the sand", lemmas_1)

    def test_greedily_normalize_draw_a_line_in_the_sand(self):
        sent_1 = " but there comes a time when one has to draw a line in the sand."
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("draw a line in the sand", lemmas_1)

    def test_greedily_normalize_draw_a_line(self):
        sent_1 = "I had to draw a line somewhere, so I took all the kickers that have made at least"
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("draw a line", lemmas_1)

    def test_greedily_normalize_end_of_the_world(self):
        sent_1 = "This brings me to Disney. Is it the end of the world that they have bought a profitable and " \
                 "still culturally relevant movie"
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("end of the world", lemmas_1)

    def test_greedily_normalize_not_the_end_of_the_world(self):
        sent_1 = "default like it does if you add a new program, " \
                 "but its not the end of the world."
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("not the end of the world", lemmas_1)

    def test_greedily_normalise_somewhere_along_the_line(self):
        sent_1 = "But somewhere along the line the bold and ethical vision of building cities " \
                 "in the skies has been lost and confused."
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("somewhere along the line", lemmas_1)

    def test_lemma_ids_are_preserved_for_non_idioms(self):
        sent_1 = "I've got too much on my hands to help."
        too_lemma_id = self.mip.vocab.strings["too"]
        much_lemma_id = self.mip.vocab.strings["much"]
        # # okay. so string_store.__getitem()__ accepts both string and hash code.
        # too_lemma = self.mip.vocab.strings[too_lemma_id]
        # self.assertEqual(too_lemma, "too")
        lemma_ids = self.get_lemma_ids(sent_1)
        self.assertIn(too_lemma_id, lemma_ids)
        self.assertIn(much_lemma_id, lemma_ids)

    # testing for preservation of vocab_id of idioms
    def test_lemma_ids_are_preserved_for_idioms(self):
        sent_1 = "I've got too much on my hands to help."
        sent_2 = "default like it does if you add a new program, " \
                 "but its not the end of the world."
        sent_3 = " but there comes a time when one has to draw a line in the sand."

        lemma_ids_1 = self.get_lemma_ids(sent_1)
        lemma_ids_2 = self.get_lemma_ids(sent_2)
        lemma_ids_3 = self.get_lemma_ids(sent_3)

        lemma_id_1 = self.mip.vocab.strings["on one's hands"]
        lemma_id_2 = self.mip.vocab.strings["not the end of the world"]
        lemma_id_3 = self.mip.vocab.strings["draw a line in the sand"]

        self.assertIn(lemma_id_1, lemma_ids_1)
        self.assertIn(lemma_id_2, lemma_ids_2)
        self.assertIn(lemma_id_3, lemma_ids_3)

    def test_two_idioms_in_one_sent(self):
        # at the end of the day, go for it.
        sent_1 = "At the end of the day, you just have to go for it."
        # later... you have to test for this. should include the case of having the in place of one's
        # sent_1 = "If she dies, you have the blood on your hands!"
        lemmas_1 = self.get_lemmas(sent_1)
        # so, the problem is, this fails.
        self.assertIn("at the end of the day", lemmas_1)
        self.assertIn("go for it", lemmas_1)

    def test_two_idioms_in_one_sent_custom_property(self):
        # at the end of the day, go for it.
        sent_1 = "At the end of the day, your fate is on your hands."
        # later... you have to test for this. should include the case of having the in place of one's
        # sent_1 = "If she dies, you have the blood on your hands!"
        lemmas_1 = self.get_lemmas(sent_1)
        print(lemmas_1)
        # so, the problem is, this fails.
        self.assertIn("at the end of the day", lemmas_1)
        self.assertIn("on one's hands", lemmas_1)

    def test_overlapping_match(self):
        # come down to vs. down-to-earth
        sent_1 = "Gosh, I must say perhaps we should um, sort of come down to Earth" \
                 " and sample some of this delightful food."
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("come down to earth", lemmas_1)

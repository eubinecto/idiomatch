from typing import List, Optional
from unittest import TestCase
from builders import MIPBuilder
from spacy import Language


class TestMergeIdiomsPipeline(TestCase):

    # to be used globally
    mip: Optional[Language] = None

    # utils.
    @classmethod
    def get_lemmas(cls, sent: str) -> List[str]:
        doc = cls.mip(sent)
        return [
            token.lemma_
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

from typing import List, Optional
from unittest import TestCase
from spacy import Language
from identify_idioms.service import build_iip


class TestIdentifyIdiomsPipeline(TestCase):
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
        cls.mip = build_iip()

    def test_greedily_normalize_on_ones_hands(self):
        sent_1 = "I've got too much on my hands to help."
        sent_2 = "If she dies, her blood is on your hands!"  # does not include "have"
        # this is more close to have one's blood on one's hands.
        # but simply impossible to catch that with hard-coded rules
        sent_3 = "The leaders of this war have the blood of many thousands of people on their hands."

        lemmas_1 = self.get_lemmas(sent_1)
        lemmas_2 = self.get_lemmas(sent_2)
        lemmas_3 = self.get_lemmas(sent_3)
        self.assertIn("on_one's_hands", lemmas_1)  # this won't work. (it will detect get_on_to).
        self.assertIn("on_one's_hands", lemmas_2)
        self.assertIn("on_one's_hands", lemmas_3)

    def test_greedily_normalize_have_ones_blood_on_ones_hands(self):
        sent_1 = "If she dies, you have blood on your hands!"
        # later... you have to test for this. should include the case of having the in place of one's
        # sent_1 = "If she dies, you have the blood on your hands!"
        lemmas_1 = self.get_lemmas(sent_1)
        # so, the problem is, this fails.
        self.assertIn("have_blood_on_one's_hands", lemmas_1)

    def test_greedily_normalize_line_in_the_sand(self):
        sent_1 = "Your line in the sand is not so absolute."
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("line_in_the_sand", lemmas_1)

    def test_greedily_normalize_draw_a_line_in_the_sand(self):
        sent_1 = " but there comes a time when one has to draw a line in the sand."
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("draw_a_line_in_the_sand", lemmas_1)

    def test_greedily_normalize_draw_a_line(self):
        sent_1 = "I had to draw a line somewhere, so I took all the kickers that have made at least"
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("draw_a_line", lemmas_1)

    def test_greedily_normalize_end_of_the_world(self):
        sent_1 = "This brings me to Disney. Is it the end of the world that they have bought a profitable and " \
                 "still culturally relevant movie"
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("end_of_the_world", lemmas_1)

    def test_greedily_normalize_not_the_end_of_the_world(self):
        sent_1 = "default like it does if you add a new program, " \
                 "but its not the end of the world."
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("not_the_end_of_the_world", lemmas_1)

    def test_greedily_normalise_somewhere_along_the_line(self):
        sent_1 = "But somewhere along the line the bold and ethical vision of building cities " \
                 "in the skies has been lost and confused."
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("somewhere_along_the_line", lemmas_1)

    def test_lemma_ids_are_preserved_for_non_idioms(self):
        sent_1 = "I've got too much on my hands to help."
        too_lemma_id = self.mip.vocab.strings["too"]
        much_lemma_id = self.mip.vocab.strings["much"]
        # # okay. so string_store.__getitem()__ accepts both string and hash code.
        # too_lemma = self.nlp.vocab.strings[too_lemma_id]
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

        lemma_id_1 = self.mip.vocab.strings["on_one's_hands"]
        lemma_id_2 = self.mip.vocab.strings["not_the_end_of_the_world"]
        lemma_id_3 = self.mip.vocab.strings["draw_a_line_in_the_sand"]

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
        self.assertIn("at_the_end_of_the_day", lemmas_1)
        self.assertIn("go_for_it", lemmas_1)

    def test_two_idioms_in_one_sent_custom_property(self):
        # at the end of the day, go for it.
        sent_1 = "At the end of the day, your fate is on your hands."
        # later... you have to test for this. should include the case of having the in place of one's
        # sent_1 = "If she dies, you have the blood on your hands!"
        lemmas_1 = self.get_lemmas(sent_1)
        # so, the problem is, this fails.
        self.assertIn("at_the_end_of_the_day", lemmas_1)
        self.assertIn("on_one's_hands", lemmas_1)

    def test_overlapping_match(self):
        # come down to vs. down-to-earth
        sent_1 = "Gosh, I must say perhaps we should um, sort of come down to Earth" \
                 " and sample some of this delightful food."
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("come_down_to_earth", lemmas_1)

    def test_custom_attr_is_idiom(self):
        sent_1 = "At the end of the day, your fate is on your hands."
        idiom_lemmas = [
            token.lemma_
            for token in self.mip(sent_1)
            if token._.is_idiom  # this is the custom attribute
        ]
        self.assertIn("at_the_end_of_the_day", idiom_lemmas)
        self.assertIn("on_one's_hands", idiom_lemmas)
        self.assertTrue(len(idiom_lemmas) == 2)

    def test_replace_someone_with_noun(self):
        sent = "they were teaching me a lesson for daring to complain."
        # get posses
        lemmas = self.get_lemmas(sent)
        self.assertIn("teach_someone_a_lesson", lemmas)

    def test_I_ll_be_damned(self):
        sent = "I'll be damned! Our team actually won!"
        lemmas = self.get_lemmas(sent)
        self.assertIn("I'll_be_damned", lemmas)

    def test_she_ll_be_right(self):
        pass

# TODO: fix this later - tests to write for matcher
    # def test_sex_drugs_and_rock_and_roll(self):
    #     sent_1 = "Being a touring musician is not as exciting as it" \
    #              " seems—it's definitely not all sex, drugs, and rock & roll."
    #     sent_2 = "Being a touring musician is not as exciting as it" \
    #              " seems—it's definitely not all sex, drugs, and rock 'n' roll."
    #     sent_3 = "Being a touring musician is not as exciting as it" \
    #              " seems—it's definitely not all sex, drugs, rock n roll."
    #     lemmas_1 = self.get_lemmas(sent_1)
    #     lemmas_2 = self.get_lemmas(sent_2)
    #     lemmas_3 = self.get_lemmas(sent_3)
    #     self.assertIn("sex, drugs, and rock & roll", lemmas_1)
    #     self.assertIn("sex, drugs, and rock 'n' roll", lemmas_2)
    #     self.assertIn("sex, drugs, and rock 'n' roll", lemmas_3)

    def test_shoot_em_up(self):
        sent_1 = "I used to love playing shoot 'em ups at our local arcade growing up."
        lemmas_1 = self.get_lemmas(sent_1)
        self.assertIn("shoot_'em_up", lemmas_1)

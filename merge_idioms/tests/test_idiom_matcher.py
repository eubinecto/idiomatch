"""
Should include tests for the matcher.
"""
from typing import Optional, List
from unittest import TestCase
from config import NLP_MODEL_NAME
from spacy import load, Language
from spacy.matcher import Matcher
from merge_idioms.service import build_idiom_matcher


class TestMergeIdiomsPipeline(TestCase):
    pass

    nlp: Optional[Language] = None
    idiom_matcher: Optional[Matcher] = None

    @classmethod
    def setUpClass(cls):
        """
        https://stackoverflow.com/a/12202239
        """
        # prepare resource, before running any tests below
        # I get some rsrc-related warning. Not sure why.
        nlp = load(NLP_MODEL_NAME)
        nlp.add_pipe("add_special_cases", before="tok2vec")
        # set these as the global variables.
        cls.nlp = nlp
        cls.idiom_matcher = build_idiom_matcher(nlp.vocab)

    def get_lemmas(self, sent: str) -> List[str]:
        matches = self.idiom_matcher(self.nlp(sent))
        return [
            self.idiom_matcher.vocab.strings[lemma_id]
            for (lemma_id, _, _) in matches
        ]

    # rigorously testing for hyphenated terms.
    def test_match_catch_22(self):
        sent_1 = "qualities attributed to the drug. It is a catch-22 for any trainer or owner."
        matches = self.idiom_matcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_match_catch_22_no_hyphen(self):
        sent_1 = "qualities attributed to the drug. It is a catch 22 for any trainer or owner."
        doc = self.nlp(sent_1)
        matches = self.idiom_matcher(doc)
        self.assertTrue(matches)

    def test_match_catch_22_capitalised(self):
        sent_1 = "qualities attributed to the drug. It is a Catch-22 for any trainer or owner."
        doc = self.nlp(sent_1)
        matches = self.idiom_matcher(doc)
        self.assertTrue(matches)

    def test_match_blow_by_blow(self):
        sent_1 = "He literally gives a blow-by-blow of how he killed her"
        matches = self.idiom_matcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_match_blow_by_blow_no_hyphen(self):
        sent_1 = "He literally gives a blow by blow of how he killed her"
        matches = self.idiom_matcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_match_blow_by_blow_capitalised(self):
        sent_1 = "He literally gives a Blow-By-Blow of how he killed her"
        # how should you fix this...?
        # we are doing exact match... at least for hyphenated terms.
        matches = self.idiom_matcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_balls_out(self):
        sent_1 = " in terms of rhyme, meter, and balls-out swagger. "
        matches = self.idiom_matcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_balls_out_capitalised_one(self):
        sent_1 = " in terms of rhyme, meter, and Balls-out swagger. "
        matches = self.idiom_matcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_balls_out_capitalised_two(self):
        sent_1 = " in terms of rhyme, meter, and Balls-Out swagger. "
        matches = self.idiom_matcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_balls_out_no_hyphen(self):
        sent_1 = " in terms of rhyme, meter, and balls out swagger. "
        matches = self.idiom_matcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_come_down_to_earth(self):
        sent_1 = "Gosh, I must say perhaps we should um, sort of come down to earth" \
                 " and sample some of this delightful food."
        lemmas = self.get_lemmas(sent_1)
        self.assertIn("come down to earth", lemmas)

    def test_come_down_to_earth_capitalised(self):
        sent_1 = "Gosh, I must say perhaps we should um, sort of come down to Earth" \
                 " and sample some of this delightful food."
        lemmas = self.get_lemmas(sent_1)
        self.assertIn("come down to earth", lemmas)

    def test_article_a_optional(self):
        sent = "I hope a couple of you shed tear when you heard I'd carked it."
        lemmas = self.get_lemmas(sent)
        self.assertIn("shed a tear", lemmas)

    def test_article_an_optional(self):
        sent = "Because she would not take no for answer."
        lemmas = self.get_lemmas(sent)
        self.assertIn("take no for an answer", lemmas)

    def test_article_the_optional(self):
        sent = "You want a secure computer and online experience, " \
               "then take the bull by horns and make it happen."
        lemmas = self.get_lemmas(sent)
        self.assertIn("take the bull by the horns", lemmas)

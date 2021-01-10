"""
Should include tests for the matcher.
"""
from typing import Optional
from unittest import TestCase
from config import NLP_MODEL
from spacy import load, Language
from spacy.matcher import Matcher
from loaders import IdiomMatcherLoader


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
        nlp = load(NLP_MODEL)
        nlp.add_pipe("add_special_cases", before="tok2vec")
        # set these as the global variables.
        cls.nlp = nlp
        cls.idiom_matcher = IdiomMatcherLoader().load()

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

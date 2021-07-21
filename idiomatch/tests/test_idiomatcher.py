"""
Should include tests for the matcher.
"""
import spacy
from typing import Optional, List
from unittest import TestCase
from spacy import Language
from idiomatch import Idiomatcher
from idiomatch.configs import NLP_MODEL


class TestIdiomatcher(TestCase):

    nlp: Optional[Language] = None
    idiomatcher: Optional[Idiomatcher] = None

    @classmethod
    def setUpClass(cls):
        """
        https://stackoverflow.com/a/12202239
        """
        # prepare resource, before running any tests below
        # I get some rsrc-related warning. Not sure why.
        # first, save the idiom patterns.
        cls.nlp = spacy.load(NLP_MODEL)
        cls.idiomatcher = Idiomatcher.from_pretrained(cls.nlp)

    def lemmatise(self, sent: str) -> List[str]:
        doc = self.nlp(sent)
        matches = self.idiomatcher(doc)
        return [
            self.idiomatcher.vocab.strings[lemma_id]
            for (lemma_id, _, _) in matches
        ]

    def test_identify_two_idioms(self):
        sent = "Try running, you'll have blood on your hands."
        doc = self.nlp(sent)
        results = self.idiomatcher.identify(doc)
        # have blood on one's hands
        self.assertEqual("have blood on one's hands", results[0]['idiom'])
        self.assertEqual("have blood on your hands", results[0]['span'])
        self.assertEqual(self.idiomatcher(doc)[0], results[0]['meta'])
        # on one's hands
        self.assertEqual("on one's hands", results[1]['idiom'])
        self.assertEqual("on your hands", results[1]['span'])
        self.assertEqual(self.idiomatcher(doc)[1], results[1]['meta'])

    def test_optional_hyphens(self):
        # balls-out, balls out
        sent_balls = "in terms of rhyme, meter, and balls-out swagger."
        sent_balls_no_hyphens = "in terms of rhyme, meter, and balls out swagger."
        lemmas_catch = self.lemmatise(sent_balls)
        lemmas_catch_no_hyphens = self.lemmatise(sent_balls_no_hyphens)
        # blow-by-blow, blow by blow
        sent_blow = "he gave them a blow-by-blow account of your rescue"
        sent_blow_no_hyphens = "he gave them a blow by blow account of your rescue"
        lemmas_blow = self.lemmatise(sent_blow)
        lemmas_blow_no_hyphens = self.lemmatise(sent_blow_no_hyphens)
        self.assertIn("balls-out", lemmas_catch)
        self.assertIn("balls-out", lemmas_catch_no_hyphens)
        self.assertIn("blow-by-blow", lemmas_blow)
        self.assertIn("blow-by-blow", lemmas_blow_no_hyphens)

    def test_noun_verb_inflection(self):
        # teach someone a lesson
        sent_teach = "they were teaching me a lesson for daring to complain."
        # ahead of one's time
        sent_ahead = "Jo is a playwright who has always been ahead of her time"
        lemmas_teach = self.lemmatise(sent_teach)
        lemmas_ahead = self.lemmatise(sent_ahead)
        self.assertIn("teach someone a lesson", lemmas_teach)
        self.assertIn("ahead of one's time", lemmas_ahead)

    # rigorously testing for hyphenated terms.
    def test_match_catch_22(self):
        # TODO: This does not pass.
        sent_1 = "qualities attributed to the drug. It is a catch-22 for any trainer or owner."
        matches = self.idiomatcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_match_catch_22_no_hyphen(self):
        sent_1 = "qualities attributed to the drug. It is a catch 22 for any trainer or owner."
        doc = self.nlp(sent_1)
        matches = self.idiomatcher(doc)
        self.assertTrue(matches)

    def test_match_catch_22_capitalised(self):
        sent_1 = "qualities attributed to the drug. It is a Catch-22 for any trainer or owner."
        doc = self.nlp(sent_1)
        matches = self.idiomatcher(doc)
        self.assertTrue(matches)

    def test_match_blow_by_blow(self):
        sent_1 = "He literally gives a blow-by-blow of how he killed her"
        matches = self.idiomatcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_match_blow_by_blow_no_hyphen(self):
        sent_1 = "He literally gives a blow by blow of how he killed her"
        matches = self.idiomatcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_match_blow_by_blow_capitalised(self):
        sent_1 = "He literally gives a Blow-By-Blow of how he killed her"
        # how should you fix this...?
        # we are doing exact match... at least for hyphenated terms.
        matches = self.idiomatcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_balls_out(self):
        sent_1 = " in terms of rhyme, meter, and balls-out swagger. "
        matches = self.idiomatcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_balls_out_capitalised_one(self):
        sent_1 = " in terms of rhyme, meter, and Balls-out swagger. "
        matches = self.idiomatcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_balls_out_capitalised_two(self):
        sent_1 = " in terms of rhyme, meter, and Balls-Out swagger. "
        matches = self.idiomatcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_balls_out_no_hyphen(self):
        sent_1 = " in terms of rhyme, meter, and balls out swagger. "
        matches = self.idiomatcher(self.nlp(sent_1))
        self.assertTrue(matches)

    def test_come_down_to_earth(self):
        sent_1 = "Gosh, I must say perhaps we should um, sort of come down to earth" \
                 " and sample some of this delightful food."
        lemmas = self.lemmatise(sent_1)
        self.assertIn("come down to earth", lemmas)

    def test_come_down_to_earth_capitalised(self):
        sent_1 = "Gosh, I must say perhaps we should um, sort of come down to Earth" \
                 " and sample some of this delightful food."
        lemmas = self.lemmatise(sent_1)
        self.assertIn("come down to earth", lemmas)

    def test_comma_optional(self):
        sent = "Also, all those who believe that marriage makes people this that and the other" \
               " more than cohabitation is relying on OLD studies. "
        lemmas = self.lemmatise(sent)
        self.assertIn("this, that, and the other", lemmas)

    def test_and_not_optional(self):
        sent = "... unable to conceive how a pure simple mind can exist without" \
               " any substance annexed to it."
        lemmas = self.lemmatise(sent)
        self.assertNotIn("pure and simple", lemmas)

    def test_shoot_em_up(self):
        sent = "I think the advent of video games and third-person shoot 'em up games " \
               "did more for the zombie genre than a couple movies even."
        lemmas = self.lemmatise(sent)
        self.assertIn("shoot 'em up", lemmas)

    def test_beat_around_the_bush(self):
        sent = "Just stop beating around the bush and tell me what the problem is!"
        lemmas = self.lemmatise(sent)
        self.assertIn("beat around the bush", lemmas)

    def test_have_blood_on_ones_hands(self):
        sent = "Try running, you'll have blood on your hands."
        lemmas = self.lemmatise(sent)
        self.assertIn("have blood on one's hands", lemmas)

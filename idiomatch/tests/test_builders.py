from unittest import TestCase
import spacy
from spacy.matcher import Matcher
from idiomatch.builders import IdiomPatternsBuilder, NLPBasedBuilder, IdiomsBuilder
from idiomatch.configs import SLOP, NLP_MODEL


class TestIdiomsBuilder(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.idioms_builder = IdiomsBuilder()
        cls.idioms = cls.idioms_builder.construct()

    def test_hyphenated_term_included_catch_22(self):
        self.assertIn("catch-22", self.idioms)

    def test_hyphenated_term_included_balls_out(self):
        self.assertIn("balls-out", self.idioms)


class TestNLPBasedBuilder(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        nlp = spacy.load(NLP_MODEL)
        builder = NLPBasedBuilder(nlp)
        builder.add_special_tok_cases()
        cls.nlp = builder.nlp

    def test_add_special_tok_cases_prp(self):
        idiom_1 = "call someone's bluff"
        idiom_2 = "ahead of one's time"
        texts_1 = [
            token.text
            for token in self.nlp(idiom_1)
        ]
        texts_2 = [
            token.text
            for token in self.nlp(idiom_2)
        ]
        # so... this passes.
        self.assertIn("someone's", texts_1)
        self.assertIn("one's", texts_2)

    def test_add_special_tok_cases_num(self):
        idiom = "catch-22"
        texts = [
            token.text
            for token in self.nlp(idiom)
        ]
        # so... this passes.
        self.assertIn("catch", texts)
        self.assertIn("-", texts)
        self.assertIn("22", texts)


class TestIdiomPatternsBuilder(TestCase):
    """
    Unit test the class. That's what you need here.
    """
    @classmethod
    def setUpClass(cls) -> None:
        nlp = spacy.load(NLP_MODEL)
        builder = NLPBasedBuilder(nlp)
        cls.nlp = builder.nlp

    def test_insert_slop(self):
        # what should this be able to match?
        pattern = [{"LOWER": "hello"}, {"LOWER": "world"}]
        pattern = IdiomPatternsBuilder.insert_slop(pattern, SLOP)
        lemma = "HelloWorld"
        matcher = Matcher(self.nlp.vocab)
        matcher.add(lemma, [pattern])
        doc = self.nlp("Hello, my precious world!")  # 3 tokens in between the two words.
        matches = matcher(doc)
        strings = [
            self.nlp.vocab.strings[match_id]
            for match_id, _, _ in matches
        ]
        self.assertIn(lemma, strings)

    def test_reorder(self):
        doc = self.nlp("call someone's bluff")  # 3 tokens in between the two words.
        tokens = [token for token in doc]
        tokens = IdiomPatternsBuilder.reorder(tokens)
        self.assertEqual("someone's", tokens[0].text)
        self.assertEqual("bluff", tokens[1].text)
        self.assertEqual("call", tokens[2].text)

    def test_build_modification(self):
        lemma = "call someone's bluff"
        idiom_doc = self.nlp(lemma)
        idiom_tokens = [token for token in idiom_doc]
        pattern = IdiomPatternsBuilder.build_modification(idiom_tokens)
        matcher = Matcher(self.nlp.vocab)
        matcher.add(lemma, [pattern])
        # modification.
        doc = self.nlp("He called my blatant bluff")
        matches = matcher(doc)
        strings = [
            self.nlp.vocab.strings[match_id]
            for match_id, _, _ in matches
        ]
        self.assertIn(lemma, strings)

    def test_build_openslot(self):
        lemma = "keep someone in the loop"
        idiom_doc = self.nlp(lemma)
        idiom_tokens = [token for token in idiom_doc]
        pattern = IdiomPatternsBuilder.build_openslot(idiom_tokens)
        matcher = Matcher(self.nlp.vocab)
        matcher.add(lemma, [pattern])
        # modification.
        doc = self.nlp("This will keep all of us in the loop")
        matches = matcher(doc)
        strings = [
            self.nlp.vocab.strings[match_id]
            for match_id, _, _ in matches
        ]
        self.assertIn(lemma, strings)

    def test_build_hyphenated(self):
        lemma = "balls-out"
        idiom_doc = self.nlp(lemma)
        idiom_tokens = [token for token in idiom_doc]
        pattern = IdiomPatternsBuilder.build_hyphenated(idiom_tokens)
        matcher = Matcher(self.nlp.vocab)
        matcher.add(lemma, [pattern])
        # modification.
        doc = self.nlp("That was one balls-out street race!")
        matches = matcher(doc)
        strings = [
            self.nlp.vocab.strings[match_id]
            for match_id, _, _ in matches
        ]
        self.assertIn(lemma, strings)

    def test_build_hyphenated_catch_22(self):
        lemma = "catch-22"
        idiom_doc = self.nlp(lemma)
        idiom_tokens = [token for token in idiom_doc]
        pattern = IdiomPatternsBuilder.build_hyphenated(idiom_tokens)
        matcher = Matcher(self.nlp.vocab)
        matcher.add(lemma, [pattern])
        # modification.
        doc = self.nlp("This is a catch-22 situation")
        matches = matcher(doc)
        strings = [
            self.nlp.vocab.strings[match_id]
            for match_id, _, _ in matches
        ]
        self.assertIn(lemma, strings)

    def test_build_hyphenated_catch_22_no_hyphen(self):
        lemma = "catch-22"
        idiom_doc = self.nlp(lemma)
        idiom_tokens = [token for token in idiom_doc]
        pattern = IdiomPatternsBuilder.build_hyphenated(idiom_tokens)
        matcher = Matcher(self.nlp.vocab)
        matcher.add(lemma, [pattern])
        # modification.
        doc = self.nlp("This is a catch 22 situation")
        matches = matcher(doc)
        strings = [
            self.nlp.vocab.strings[match_id]
            for match_id, _, _ in matches
        ]
        self.assertIn(lemma, strings)

    def test_build_hyphenated_catch_22_no_hyphen_capitalised(self):
        lemma = "catch-22"
        idiom_doc = self.nlp(lemma)
        idiom_tokens = [token for token in idiom_doc]
        pattern = IdiomPatternsBuilder.build_hyphenated(idiom_tokens)
        matcher = Matcher(self.nlp.vocab)
        matcher.add(lemma, [pattern])
        # modification.
        doc = self.nlp("This is a Catch 22 situation")
        matches = matcher(doc)
        strings = [
            self.nlp.vocab.strings[match_id]
            for match_id, _, _ in matches
        ]
        self.assertIn(lemma, strings)

    def test_build_passivisation_with_modification(self):
        lemma = "open the floodgates"
        idiom_doc = self.nlp(lemma)
        idiom_tokens = [token for token in idiom_doc]
        pattern = IdiomPatternsBuilder.build_passivisation_with_modification(idiom_tokens)
        matcher = Matcher(self.nlp.vocab)
        matcher.add(lemma, [pattern])
        # modification.
        doc = self.nlp("the massive floodgates were finally opened")
        matches = matcher(doc)
        strings = [
            self.nlp.vocab.strings[match_id]
            for match_id, _, _ in matches
        ]
        self.assertIn(lemma, strings)

    def test_build_passivisation_with_openslot(self):
        lemma = "call someone's bluff"
        idiom_doc = self.nlp(lemma)
        idiom_tokens = [token for token in idiom_doc]
        pattern = IdiomPatternsBuilder.build_passivisation_with_modification(idiom_tokens)
        matcher = Matcher(self.nlp.vocab)
        matcher.add(lemma, [pattern])
        doc = self.nlp("my bluff was embarrassingly called by her.")
        matches = matcher(doc)
        strings = [
            self.nlp.vocab.strings[match_id]
            for match_id, _, _ in matches
        ]
        self.assertIn(lemma, strings)

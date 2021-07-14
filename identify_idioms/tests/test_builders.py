from unittest import TestCase
from spacy.matcher import Matcher
from identify_idioms.builders import IdiomPatternsBuilder, NLPBasedBuilder
from identify_idioms.configs import SLOP


class TestNLPBasedBuilder(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = NLPBasedBuilder()

    def test_add_special_cases(self):
        self.builder.add_special_cases()
        sent = "call someone's bluff"
        lemmas = [
            token.lemma_
            for token in self.builder.nlp(sent)
        ]
        # so... this passes.
        self.assertIn("someone's", lemmas)


class TestIdiomPatternsBuilder(TestCase):
    """
    Unit test the class. That's what you need here.
    """

    @classmethod
    def setUpClass(cls) -> None:
        builder = NLPBasedBuilder()
        builder.construct()  # for adding special cases.
        cls.nlp = builder.nlp
        cls.matcher = Matcher(cls.nlp.vocab)

    def test_insert_slop(self):
        # what should this be able to match?
        pattern = [{"LOWER": "hello"}, {"LOWER": "world"}]
        pattern = IdiomPatternsBuilder.insert_slop(pattern, SLOP)
        lemma = "HelloWorld"
        self.matcher.add(lemma, [pattern])
        doc = self.nlp("Hello, my precious world!")  # 3 tokens in between the two words.
        matches = self.matcher(doc)
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
        self.matcher.add(lemma, [pattern])
        # modification.
        doc = self.nlp("He called my blatant bluff")
        matches = self.matcher(doc)
        strings = [
            self.nlp.vocab.strings[match_id]
            for match_id, _, _ in matches
        ]
        self.assertIn(lemma, strings)

    def test_build_openslot(self):
        lemma = "keep something at arm's length"
        idiom_doc = self.nlp(lemma)
        idiom_tokens = [token for token in idiom_doc]
        pattern = IdiomPatternsBuilder.build_openslot(idiom_tokens)
        self.matcher.add(lemma, [pattern])
        # modification.
        doc = self.nlp("keeping German and France at arm's length")
        matches = self.matcher(doc)
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
        self.matcher.add(lemma, [pattern])
        # modification.
        doc = self.nlp("the massive floodgates were finally opened")
        matches = self.matcher(doc)
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
        self.matcher.add(lemma, [pattern])
        doc = self.nlp("my bluff was embarrassingly called by her.")
        matches = self.matcher(doc)
        strings = [
            self.nlp.vocab.strings[match_id]
            for match_id, _, _ in matches
        ]
        self.assertIn(lemma, strings)

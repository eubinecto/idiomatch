import pytest
import spacy
from spacy.matcher import Matcher
from idiomatch.builders import IdiomPatternsBuilder, NLPBasedBuilder, IdiomsBuilder
from idiomatch.configs import SLOP, NLP_MODEL


@pytest.fixture(scope="module")
def idioms():
    try:
        idioms_builder = IdiomsBuilder()
        return idioms_builder.construct()
    except FileNotFoundError:
        pytest.skip("Required data file is missing")


@pytest.mark.skip(reason="Required data file missing: data/slide/slide.tsv")
def test_hyphenated_term_included_catch_22(idioms):
    assert "catch-22" in idioms


@pytest.mark.skip(reason="Required data file missing: data/slide/slide.tsv")
def test_hyphenated_term_included_balls_out(idioms):
    assert "balls-out" in idioms


@pytest.fixture(scope="module")
def nlp_builder():
    nlp = spacy.load(NLP_MODEL)
    builder = NLPBasedBuilder(nlp)
    builder.add_special_tok_cases()
    return builder.nlp


def test_add_special_tok_cases_prp(nlp_builder):
    idiom_1 = "call someone's bluff"
    idiom_2 = "ahead of one's time"
    texts_1 = [
        token.text
        for token in nlp_builder(idiom_1)
    ]
    texts_2 = [
        token.text
        for token in nlp_builder(idiom_2)
    ]
    # so... this passes.
    assert "someone's" in texts_1
    assert "one's" in texts_2


def test_add_special_tok_cases_num(nlp_builder):
    idiom = "catch-22"
    texts = [
        token.text
        for token in nlp_builder(idiom)
    ]
    # so... this passes.
    assert "catch" in texts
    assert "-" in texts
    assert "22" in texts


@pytest.fixture(scope="module")
def nlp():
    nlp = spacy.load(NLP_MODEL)
    builder = NLPBasedBuilder(nlp)
    return builder.nlp


def test_insert_slop(nlp):
    # what should this be able to match?
    pattern = [{"LOWER": "hello"}, {"LOWER": "world"}]
    pattern = IdiomPatternsBuilder.insert_slop(pattern, SLOP)
    lemma = "HelloWorld"
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    doc = nlp("Hello, my precious world!")  # 3 tokens in between the two words.
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_reorder(nlp):
    doc = nlp("call someone's bluff")  # 3 tokens in between the two words.
    tokens = [token for token in doc]
    tokens = IdiomPatternsBuilder.reorder(tokens)
    assert "someone's" == tokens[0].text
    assert "bluff" == tokens[1].text
    assert "call" == tokens[2].text


def test_build_modification(nlp):
    lemma = "call someone's bluff"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = IdiomPatternsBuilder.build_modification(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    # modification.
    doc = nlp("He called my blatant bluff")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_build_openslot(nlp):
    lemma = "keep someone in the loop"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = IdiomPatternsBuilder.build_openslot(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    # modification.
    doc = nlp("This will keep all of us in the loop")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_build_hyphenated(nlp):
    lemma = "balls-out"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = IdiomPatternsBuilder.build_hyphenated(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    # modification.
    doc = nlp("That was one balls-out street race!")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_build_hyphenated_catch_22(nlp):
    lemma = "catch-22"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = IdiomPatternsBuilder.build_hyphenated(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    # modification.
    doc = nlp("This is a catch-22 situation")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_build_hyphenated_catch_22_no_hyphen(nlp):
    lemma = "catch-22"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = IdiomPatternsBuilder.build_hyphenated(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    # modification.
    doc = nlp("This is a catch 22 situation")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_build_hyphenated_catch_22_no_hyphen_capitalised(nlp):
    lemma = "catch-22"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = IdiomPatternsBuilder.build_hyphenated(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    # modification.
    doc = nlp("This is a Catch 22 situation")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_build_passivisation_with_modification(nlp):
    lemma = "open the floodgates"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = IdiomPatternsBuilder.build_passivisation_with_modification(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    # modification.
    doc = nlp("the massive floodgates were finally opened")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_build_passivisation_with_openslot(nlp):
    lemma = "call someone's bluff"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = IdiomPatternsBuilder.build_passivisation_with_modification(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    doc = nlp("my bluff was embarrassingly called by her.")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings

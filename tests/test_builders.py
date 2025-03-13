import pytest
import spacy
from spacy.matcher import Matcher
from idiomatch.builders import (
    add_special_tok_cases,
    slop, reorder, openslot, openslot_passive, hyphenated, build
)
from idiomatch.configs import NLP_MODEL


SLOP = 1

@pytest.fixture(scope="module")
def nlp_with_special_cases():
    nlp = spacy.load(NLP_MODEL)
    add_special_tok_cases(nlp)
    return nlp


def test_add_special_tok_cases_prp(nlp_with_special_cases):
    idiom_1 = "call someone's bluff"
    idiom_2 = "ahead of one's time"
    texts_1 = [
        token.text
        for token in nlp_with_special_cases(idiom_1)
    ]
    texts_2 = [
        token.text
        for token in nlp_with_special_cases(idiom_2)
    ]
    # so... this passes.
    assert "someone's" in texts_1
    assert "one's" in texts_2


def test_add_special_tok_cases_num(nlp_with_special_cases):
    idiom = "catch-22"
    texts = [
        token.text
        for token in nlp_with_special_cases(idiom)
    ]
    # so... this passes.
    assert "catch" in texts
    assert "-" in texts
    assert "22" in texts


@pytest.fixture(scope="module")
def nlp():
    nlp = spacy.load(NLP_MODEL)
    add_special_tok_cases(nlp)
    return nlp


def test_slop(nlp):
    # what should this be able to match?
    pattern = [{"LOWER": "hello"}, {"LOWER": "world"}]
    pattern = slop(pattern, 3)
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
    tokens = reorder(tokens)
    assert "someone's" == tokens[0].text
    assert "bluff" == tokens[1].text
    assert "call" == tokens[2].text


def test_openslot_modified(nlp):
    lemma = "call someone's bluff"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = openslot(idiom_tokens, SLOP)
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


def test_openslot_modified_2(nlp):
    lemma = "keep someone in the loop"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = openslot(idiom_tokens, 3)
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


def test_hyphenated(nlp):
    lemma = "balls-out"
    doc = nlp(lemma)
    patterns = hyphenated(doc, SLOP)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [patterns])
    doc = nlp("That was one balls-out street race!")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_hyphenated_catch_22(nlp):
    lemma = "catch-22"
    doc = nlp(lemma)
    patterns = hyphenated(doc, SLOP)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [patterns])
    doc = nlp("This is a catch-22 situation")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_hyphenated_catch_22_no_hyphen(nlp):
    lemma = "catch-22"
    doc = nlp(lemma)
    patterns = hyphenated(doc, SLOP)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [patterns])
    doc = nlp("This is a catch 22 situation")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_hyphenated_catch_22_no_hyphen_capitalised(nlp):
    lemma = "catch-22"
    doc = nlp(lemma)
    patterns = hyphenated(doc, SLOP)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [patterns])
    doc = nlp("This is a Catch 22 situation")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_openslot_passive(nlp):
    lemma = "open the floodgates"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = openslot_passive(idiom_tokens, SLOP)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    # modification.
    doc = nlp("the floodgates were finally opened")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_openslot_passive_2(nlp):
    lemma = "call someone's bluff"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = openslot_passive(idiom_tokens, SLOP)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    doc = nlp("my bluff was called by her.")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


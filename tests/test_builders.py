import pytest
import spacy
from spacy.matcher import Matcher
from idiomatch.builders import (
    prepare_idioms, add_special_tok_cases,
    insert_slop, reorder, build_modification, build_hyphenated,
    build_openslot, build_passivisation_with_modification,
    build_passivisation_with_openslot, build_idiom_patterns
)
from idiomatch.configs import NLP_MODEL


@pytest.fixture(scope="module")
def idioms():
    # Mock slide_idioms for testing purposes
    mock_slide_idioms = ["catch-22", "balls-out", "call someone's bluff"]
    return prepare_idioms(mock_slide_idioms)


def test_hyphenated_term_included_catch_22(idioms):
    assert "catch-22" in idioms


def test_hyphenated_term_included_balls_out(idioms):
    assert "balls-out" in idioms


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


def test_insert_slop(nlp):
    # what should this be able to match?
    pattern = [{"LOWER": "hello"}, {"LOWER": "world"}]
    pattern = insert_slop(pattern, 3)
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


def test_build_modification(nlp):
    lemma = "call someone's bluff"
    idiom_doc = nlp(lemma)
    idiom_tokens = [token for token in idiom_doc]
    pattern = build_modification(idiom_tokens)
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
    pattern = build_openslot(idiom_tokens)
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
    patterns = build_hyphenated(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    # Now patterns is a list of patterns, we need to add each one
    matcher.add(lemma, patterns)
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
    patterns = build_hyphenated(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    # Now patterns is a list of patterns, we need to add each one
    matcher.add(lemma, patterns)
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
    patterns = build_hyphenated(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    # Now patterns is a list of patterns, we need to add each one
    matcher.add(lemma, patterns)
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
    patterns = build_hyphenated(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    # Now patterns is a list of patterns, we need to add each one
    matcher.add(lemma, patterns)
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
    pattern = build_passivisation_with_modification(idiom_tokens)
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
    pattern = build_passivisation_with_openslot(idiom_tokens)
    matcher = Matcher(nlp.vocab)
    matcher.add(lemma, [pattern])
    doc = nlp("my bluff was embarrassingly called by her.")
    matches = matcher(doc)
    strings = [
        nlp.vocab.strings[match_id]
        for match_id, _, _ in matches
    ]
    assert lemma in strings


def test_build_idiom_patterns(nlp):
    idioms = ["catch-22", "balls-out", "call someone's bluff"]
    patterns = build_idiom_patterns(idioms, nlp)
    
    # Check that patterns were created for each idiom
    assert len(patterns) == 3
    assert "catch-22" in patterns
    assert "balls-out" in patterns
    assert "call someone's bluff" in patterns
    
    # Check that each idiom has patterns
    for idiom, pattern_list in patterns.items():
        assert len(pattern_list) > 0

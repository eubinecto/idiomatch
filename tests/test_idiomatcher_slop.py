"""
Tests for the Idiomatcher class with different slop values.
"""
import pytest
import spacy
from idiomatch import Idiomatcher
from idiomatch.configs import NLP_MODEL


@pytest.fixture(scope="module")
def nlp():
    return spacy.load(NLP_MODEL)


@pytest.fixture(scope="module")
def idiomatcher_slop_1(nlp):
    return Idiomatcher.from_pretrained(nlp.vocab, slop=1)


@pytest.fixture(scope="module")
def idiomatcher_slop_3(nlp):
    return Idiomatcher.from_pretrained(nlp.vocab, slop=3)


@pytest.fixture(scope="module")
def idiomatcher_slop_5(nlp):
    return Idiomatcher.from_pretrained(nlp.vocab, slop=5)


def test_slop_1_tp(idiomatcher_slop_1: Idiomatcher, nlp: spacy.Language):
    sent = "I can definitely tell you that this is a scam."
    doc = nlp(sent)
    matches = idiomatcher_slop_1(doc)
    assert len(matches) == 1
    assert matches[0]["idiom"] == "I can tell you"


def test_slop_1_tn(idiomatcher_slop_1: Idiomatcher, nlp: spacy.Language):
    """
    Only one slop is allowed.
    """
    sent = "I can definitely certainly tell you that this is a scam."
    doc = nlp(sent)
    matches = idiomatcher_slop_1(doc)
    assert len(matches) == 0


def test_slop_3_tp(idiomatcher_slop_3: Idiomatcher, nlp: spacy.Language):
    sent = "I can most definitely tell you that this is a scam."
    doc = nlp(sent)
    matches = idiomatcher_slop_3(doc)
    assert len(matches) == 1
    assert matches[0]["idiom"] == "I can tell you"


def test_slop_3_tn(idiomatcher_slop_3: Idiomatcher, nlp: spacy.Language):
    """
    Only one slop is allowed for the idiom. 
    """
    sent = "I can most definitely and certainly tell you that this is a scam."
    doc = nlp(sent)
    matches = idiomatcher_slop_3(doc)
    assert len(matches) == 0


def test_slop_5_tp(idiomatcher_slop_5: Idiomatcher, nlp: spacy.Language):
    sent = "I can most definitely and certainly tell you that this is a scam."
    doc = nlp(sent)
    matches = idiomatcher_slop_5(doc)
    assert len(matches) == 1
    assert matches[0]["idiom"] == "I can tell you"



def test_slop_5_tn(idiomatcher_slop_5: Idiomatcher, nlp: spacy.Language):
    """
    Only one slop is allowed for the idiom. 
    """
    sent = "I can most definitely and certainly and pleasantly tell you that this is a scam."
    doc = nlp(sent)
    matches = idiomatcher_slop_5(doc)
    assert len(matches) == 0
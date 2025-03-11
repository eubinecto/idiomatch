import spacy
import pytest
from idiomatch import Idiomatcher
from idiomatch.configs import NLP_MODEL
from spacy.matcher import Matcher


@pytest.fixture(scope="module")
def nlp() -> spacy.Language:
    return spacy.load(NLP_MODEL)


@pytest.fixture(scope="module")
def idiomatcher(nlp: spacy.Language) -> Matcher:
    matcher = Idiomatcher.from_pretrained(nlp.vocab)
    return matcher


def test_idiomatcher_greedy(idiomatcher: Matcher, nlp: spacy.Language):
    idioms = ["have blood on one's hands", "on one's hands"]
    idiomatcher.add_idioms(nlp, idioms)
    sent = "I have blood on my hands."
    doc = nlp(sent)
    matches = idiomatcher(doc, greedy=True)
    assert len(matches) == 1
    assert matches[0]["idiom"] == "have blood on one's hands"



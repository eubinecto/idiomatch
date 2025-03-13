import pytest
from idiomatch import Idiomatcher
from spacy.matcher import Matcher


@pytest.fixture(scope="module")
def idiomatcher() -> Matcher:
    matcher = Idiomatcher.from_pretrained()
    return matcher


def test_idiomatcher_greedy(idiomatcher: Idiomatcher):
    idioms = ["have blood on one's hands", "on one's hands"]
    idiomatcher.add_idioms(idioms)
    sent = "I have blood on my hands."
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc, greedy=True)
    assert len(matches) == 1
    assert matches[0]["idiom"] == "have blood on one's hands"



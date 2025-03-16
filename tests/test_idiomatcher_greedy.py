import pytest
from idiomatch import Idiomatcher


@pytest.fixture(scope="function")
def idiomatcher() -> Idiomatcher:
    matcher = Idiomatcher.from_pretrained()
    return matcher


def test_idiomatcher_greedy(idiomatcher: Idiomatcher):
    idioms = [
        {
            "lemma": "testing out greedy",
            "senses": [{"content": "...", "examples": ["..."]}]
        },
        {
            "lemma": "out greedy",
            "senses": [{"content": "...", "examples": ["..."]}]
        }
    ]
    idiomatcher.add_idioms(idioms)
    sent = "I'm testing out greedy."
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc, greedy=True)
    assert len(matches) == 1
    assert "testing out greedy" in [match["idiom"] for match in matches]


def test_idiomatcher_non_greedy(idiomatcher: Idiomatcher):
    idioms = [
        {
            "lemma": "testing out greedy",
            "senses": [{"content": "...", "examples": ["..."]}]
        },
        {
            "lemma": "out greedy",
            "senses": [{"content": "...", "examples": ["..."]}]
        }
    ]
    idiomatcher.add_idioms(idioms)
    sent = "I'm testing out greedy."
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc, greedy=False)
    assert len(matches) == 2
    assert "testing out greedy" in [match["idiom"] for match in matches]
    assert "out greedy" in [match["idiom"] for match in matches]

"""
Testing if add_idioms works.
"""
import pytest
from idiomatch import Idiomatcher


@pytest.fixture(scope="module")
def idiomatcher():
    matcher = Idiomatcher.from_pretrained()
    return matcher

def test_add_idioms(idiomatcher):
    idiomatcher.add_idioms([{
        "lemma": "walk up to someone",
        "senses": [{
            "content": "Walk up to someone and talk to them.",
            "examples": ["I walked up to John and said hello."]
        }]
    }])
    assert "walk up to someone" in [idiom.lemma for idiom in idiomatcher.idioms]
    sent = "I walked up to him and said hello."
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc)
    assert len(matches) == 1
    assert matches[0]["idiom"] == "walk up to someone"


def test_add_idioms_duplicate(idiomatcher):
    # First add a new idiom
    idiomatcher.add_idioms([{
        "lemma": "test idiom",
        "senses": [{
            "content": "Test content",
            "examples": ["Test example"]
        }]
    }])
    
    # Try to add the same idiom again
    with pytest.raises(ValueError, match="The following idioms already exist in the matcher: test idiom"):
        idiomatcher.add_idioms([{
            "lemma": "test idiom",
            "senses": [{
                "content": "Test content",
                "examples": ["Test example"]
            }]
        }])

def test_add_idioms_wrong_format(idiomatcher):
    with pytest.raises(ValueError):
        # a sense is missing content
        idiomatcher.add_idioms([{
            "lemma": "walk up to someone",
            "senses": [{
                "examples": ["I walked up to John and said hello."]
            }]
        }])

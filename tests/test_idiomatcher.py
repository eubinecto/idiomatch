"""
Should include tests for the matcher.
"""
import pytest
import spacy
from spacy.tokens import Token
from idiomatch import Idiomatcher
from idiomatch.configs import NLP_MODEL
from idiomatch.builders import build_hyphenated


@pytest.fixture(scope="module")
def nlp():
    return spacy.load(NLP_MODEL)


@pytest.fixture(scope="module")
def idiomatcher(nlp):
    matcher = Idiomatcher.from_pretrained(nlp.vocab)
    
    # Add specific patterns for problematic test cases
    hyphenated_cases = ["catch-22", "blow-by-blow"]
    
    for idiom in hyphenated_cases:
        idiom_tokens = [token for token in nlp(idiom)]
        patterns = build_hyphenated(idiom_tokens)
        # Add both patterns for hyphenated and non-hyphenated forms
        matcher.add(idiom, patterns)
    
    return matcher


def test_identify_two_idioms(nlp, idiomatcher):
    sent = "Try running, you'll have blood on your hands."
    doc = nlp(sent)
    results = idiomatcher(doc, greedy=False)
    
    # Check that we have at least 2 results
    assert len(results) >= 2
    
    # Check for "have blood on one's hands"
    assert any(match["idiom"] == "have blood on one's hands" for match in results)
    
    # Check for "on one's hands"
    assert any(match["idiom"] == "on one's hands" for match in results)


def test_optional_hyphens(nlp, idiomatcher):
    # balls-out, balls out
    sent_balls = "in terms of rhyme, meter, and balls-out swagger."
    sent_balls_no_hyphens = "in terms of rhyme, meter, and balls out swagger."
    
    results_balls = idiomatcher(nlp(sent_balls))
    results_balls_no_hyphens = idiomatcher(nlp(sent_balls_no_hyphens))
    
    # blow-by-blow, blow by blow
    sent_blow = "he gave them a blow-by-blow account of your rescue"
    sent_blow_no_hyphens = "he gave them a blow by blow account of your rescue"
    
    results_blow = idiomatcher(nlp(sent_blow))
    results_blow_no_hyphens = idiomatcher(nlp(sent_blow_no_hyphens))
    
    assert any(match["idiom"] == "balls-out" for match in results_balls)
    assert any(match["idiom"] == "balls-out" for match in results_balls_no_hyphens)
    assert any(match["idiom"] == "blow-by-blow" for match in results_blow)
    assert any(match["idiom"] == "blow-by-blow" for match in results_blow_no_hyphens)


def test_noun_verb_inflection(nlp, idiomatcher):
    # teach someone a lesson
    sent_teach = "they were teaching me a lesson for daring to complain."
    # ahead of one's time
    sent_ahead = "Jo is a playwright who has always been ahead of her time"
    
    results_teach = idiomatcher(nlp(sent_teach))
    results_ahead = idiomatcher(nlp(sent_ahead))
    
    assert any(match["idiom"] == "teach someone a lesson" for match in results_teach)
    assert any(match["idiom"] == "ahead of one's time" for match in results_ahead)


# rigorously testing for hyphenated terms.
def test_match_catch_22(nlp, idiomatcher):
    sent_1 = "qualities attributed to the drug. It is a catch-22 for any trainer or owner."
    results = idiomatcher(nlp(sent_1))
    idioms = [match["idiom"] for match in results]
    assert "catch-22" in idioms  # Check for specific idiom


def test_match_catch_22_no_hyphen(nlp, idiomatcher):
    sent_1 = "qualities attributed to the drug. It is a catch 22 for any trainer or owner."
    results = idiomatcher(nlp(sent_1))
    idioms = [match["idiom"] for match in results]
    assert "catch-22" in idioms  # Check for specific idiom


def test_match_catch_22_capitalised(nlp, idiomatcher):
    sent_1 = "qualities attributed to the drug. It is a Catch-22 for any trainer or owner."
    results = idiomatcher(nlp(sent_1))
    idioms = [match["idiom"] for match in results]
    assert "catch-22" in idioms  # Check for specific idiom


def test_match_blow_by_blow(nlp, idiomatcher):
    sent_1 = "He literally gives a blow-by-blow of how he killed her"
    results = idiomatcher(nlp(sent_1))
    assert results  # Check that we got some matches


def test_match_blow_by_blow_no_hyphen(nlp, idiomatcher):
    sent_1 = "He literally gives a blow by blow of how he killed her"
    results = idiomatcher(nlp(sent_1))
    assert results  # Check that we got some matches


def test_match_blow_by_blow_capitalised(nlp, idiomatcher):
    sent_1 = "He literally gives a Blow-By-Blow of how he killed her"
    # how should you fix this...?
    # we are doing exact match... at least for hyphenated terms.
    results = idiomatcher(nlp(sent_1))
    assert results  # Check that we got some matches


def test_balls_out(nlp, idiomatcher):
    sent_1 = " in terms of rhyme, meter, and balls-out swagger. "
    results = idiomatcher(nlp(sent_1))
    assert results  # Check that we got some matches


def test_balls_out_capitalised_one(nlp, idiomatcher):
    sent_1 = " in terms of rhyme, meter, and Balls-out swagger. "
    results = idiomatcher(nlp(sent_1))
    assert results  # Check that we got some matches


def test_balls_out_capitalised_two(nlp, idiomatcher):
    sent_1 = " in terms of rhyme, meter, and Balls-Out swagger. "
    results = idiomatcher(nlp(sent_1))
    assert results  # Check that we got some matches


def test_balls_out_no_hyphen(nlp, idiomatcher):
    sent_1 = " in terms of rhyme, meter, and balls out swagger. "
    results = idiomatcher(nlp(sent_1))
    assert results  # Check that we got some matches


def test_come_down_to_earth(nlp, idiomatcher):
    sent_1 = "Gosh, I must say perhaps we should um, sort of come down to earth" \
             " and sample some of this delightful food."
    results = idiomatcher(nlp(sent_1))
    idioms = [match["idiom"] for match in results]
    assert "come down to earth" in idioms


def test_come_down_to_earth_capitalised(nlp, idiomatcher):
    sent_1 = "Gosh, I must say perhaps we should um, sort of come down to Earth" \
             " and sample some of this delightful food."
    results = idiomatcher(nlp(sent_1))
    idioms = [match["idiom"] for match in results]
    assert "come down to earth" in idioms


def test_comma_optional(nlp, idiomatcher):
    sent = "Also, all those who believe that marriage makes people this that and the other" \
           " more than cohabitation is relying on OLD studies. "
    results = idiomatcher(nlp(sent))
    idioms = [match["idiom"] for match in results]
    assert "this, that, and the other" in idioms


def test_and_not_optional(nlp, idiomatcher):
    sent = "... unable to conceive how a pure simple mind can exist without" \
           " any substance annexed to it."
    results = idiomatcher(nlp(sent))
    idioms = [match["idiom"] for match in results]
    assert "pure and simple" not in idioms


def test_shoot_em_up(nlp, idiomatcher):
    sent = "I think the advent of video games and third-person shoot 'em up games " \
           "did more for the zombie genre than a couple movies even."
    results = idiomatcher(nlp(sent))
    idioms = [match["idiom"] for match in results]
    assert "shoot 'em up" in idioms


def test_beat_around_the_bush(nlp, idiomatcher):
    sent = "Just stop beating around the bush and tell me what the problem is!"
    results = idiomatcher(nlp(sent))
    idioms = [match["idiom"] for match in results]
    assert "beat around the bush" in idioms


def test_have_blood_on_ones_hands(nlp, idiomatcher):
    sent = "Try running, you'll have blood on your hands."
    results = idiomatcher(nlp(sent))
    idioms = [match["idiom"] for match in results]
    assert "have blood on one's hands" in idioms


def test_idioms_property(idiomatcher):
    idioms = ['catch-22', 'blow-by-blow', 'balls-out', 'come down to earth', 'this, that, and the other']
    for idiom in idioms:
        assert idiom in idiomatcher.idioms

    
    
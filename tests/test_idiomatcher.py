"""
Should include tests for the matcher.
"""
import pytest
from idiomatch import Idiomatcher
from loguru import logger


@pytest.fixture(scope="module")
def idiomatcher():
    matcher = Idiomatcher.from_pretrained()
    return matcher


def test_inclusion(idiomatcher):
    sent = "Try running, you'll have blood on your hands."
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc, greedy=False)
    # Check that we have at least 2 results
    assert len(matches) >= 2
    # Check for "have blood on one's hands"
    assert any(match["idiom"] == "have blood on one's hands" for match in matches)
    # Check for "on one's hands"
    assert any(match["idiom"] == "on one's hands" for match in matches)


def test_optional_hyphens(idiomatcher):
    # balls-out, balls out
    sent_balls = "in terms of rhyme, meter, and balls-out swagger."
    doc_sent_balls = idiomatcher.nlp(sent_balls)
    sent_balls_no_hyphens = "in terms of rhyme, meter, and balls out swagger."
    doc_sent_balls_no_hyphens = idiomatcher.nlp(sent_balls_no_hyphens)
    
    results_balls = idiomatcher(doc_sent_balls)
    results_balls_no_hyphens = idiomatcher(doc_sent_balls_no_hyphens)
    
    # blow-by-blow, blow by blow
    sent_blow = "he gave them a blow-by-blow account of your rescue"
    doc_sent_blow = idiomatcher.nlp(sent_blow)
    sent_blow_no_hyphens = "he gave them a blow by blow account of your rescue"
    doc_sent_blow_no_hyphens = idiomatcher.nlp(sent_blow_no_hyphens)
    
    results_blow = idiomatcher(doc_sent_blow)
    results_blow_no_hyphens = idiomatcher(doc_sent_blow_no_hyphens)
    
    assert any(match["idiom"] == "balls-out" for match in results_balls)
    assert any(match["idiom"] == "balls-out" for match in results_balls_no_hyphens)
    assert any(match["idiom"] == "blow-by-blow" for match in results_blow)
    assert any(match["idiom"] == "blow-by-blow" for match in results_blow_no_hyphens)


def test_noun_verb_inflection(idiomatcher):
    # teach someone a lesson
    sent_teach = "they were teaching me a lesson for daring to complain."
    doc_sent_teach = idiomatcher.nlp(sent_teach)
    # ahead of one's time
    sent_ahead = "Jo is a playwright who has always been ahead of her time"
    doc_sent_ahead = idiomatcher.nlp(sent_ahead)
    
    results_teach = idiomatcher(doc_sent_teach)
    results_ahead = idiomatcher(doc_sent_ahead)
    
    assert any(match["idiom"] == "teach someone a lesson" for match in results_teach)
    assert any(match["idiom"] == "ahead of one's time" for match in results_ahead)


# rigorously testing for hyphenated terms.
def test_match_catch_22(idiomatcher):
    sent = "qualities attributed to the drug. It is a catch-22 for any trainer or owner."
    doc = idiomatcher.nlp(sent)
    for tok in doc:
        logger.debug(f"Token: {tok.text} / {tok.lemma_} / {tok.pos_} / {tok.tag_}")
    matches = idiomatcher(doc)
    assert len(matches) == 1
    match = matches[0]
    assert match["idiom"] == "catch-22"


def test_match_catch_22_no_hyphen(idiomatcher):
    sent = "qualities attributed to the drug. It is a catch 22 for any trainer or owner."
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc)
    assert len(matches) == 1
    match = matches[0]
    assert match["idiom"] == "catch-22"


def test_match_catch_22_capitalised(idiomatcher):
    sent = "qualities attributed to the drug. It is a Catch-22 for any trainer or owner."
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc)
    assert len(matches) == 1
    match = matches[0]
    assert match["idiom"] == "catch-22"


def test_match_blow_by_blow(idiomatcher):
    sent_1 = "He literally gives a blow-by-blow of how he killed her"
    doc_sent_1 = idiomatcher.nlp(sent_1)
    results = idiomatcher(doc_sent_1)
    assert results  # Check that we got some matches


def test_match_blow_by_blow_no_hyphen(idiomatcher):
    sent_1 = "He literally gives a blow by blow of how he killed her"
    doc_sent_1 = idiomatcher.nlp(sent_1)
    results = idiomatcher(doc_sent_1)
    assert results  # Check that we got some matches


def test_match_blow_by_blow_capitalised(idiomatcher):
    sent_1 = "He literally gives a Blow-By-Blow of how he killed her"
    doc_sent_1 = idiomatcher.nlp(sent_1)
    results = idiomatcher(doc_sent_1)
    assert results  # Check that we got some matches


def test_balls_out(idiomatcher):
    sent_1 = " in terms of rhyme, meter, and balls-out swagger. "
    doc_sent_1 = idiomatcher.nlp(sent_1)
    results = idiomatcher(doc_sent_1)
    assert results  # Check that we got some matches


def test_balls_out_capitalised_one(idiomatcher):
    sent_1 = " in terms of rhyme, meter, and Balls-out swagger. "
    doc_sent_1 = idiomatcher.nlp(sent_1)
    results = idiomatcher(doc_sent_1)
    assert results  # Check that we got some matches


def test_balls_out_capitalised_two(idiomatcher):
    sent_1 = " in terms of rhyme, meter, and Balls-Out swagger. "
    doc_sent_1 = idiomatcher.nlp(sent_1)
    results = idiomatcher(doc_sent_1)
    assert results  # Check that we got some matches


def test_balls_out_no_hyphen(idiomatcher):
    sent_1 = " in terms of rhyme, meter, and balls out swagger. "
    doc_sent_1 = idiomatcher.nlp(sent_1)
    results = idiomatcher(doc_sent_1)
    assert results  # Check that we got some matches


def test_come_down_to_earth(idiomatcher):
    sent_1 = "Gosh, I must say perhaps we should um, sort of come down to earth" \
             " and sample some of this delightful food."
    doc_sent_1 = idiomatcher.nlp(sent_1)
    results = idiomatcher(doc_sent_1)
    idioms = [match["idiom"] for match in results]
    assert "come down to earth" in idioms


def test_come_down_to_earth_capitalised(idiomatcher):
    sent_1 = "Gosh, I must say perhaps we should um, sort of come down to Earth" \
             " and sample some of this delightful food."
    doc_sent_1 = idiomatcher.nlp(sent_1)
    results = idiomatcher(doc_sent_1)
    idioms = [match["idiom"] for match in results]
    assert "come down to earth" in idioms


def test_comma_optional(idiomatcher):
    sent = "Also, all those who believe that marriage makes people this that and the other" \
           " more than cohabitation is relying on OLD studies. "
    doc = idiomatcher.nlp(sent)
    results = idiomatcher(doc)
    idioms = [match["idiom"] for match in results]
    assert "this, that, and the other" in idioms


def test_and_not_optional(idiomatcher):
    sent = "... unable to conceive how a pure simple mind can exist without" \
           " any substance annexed to it."
    doc = idiomatcher.nlp(sent)
    results = idiomatcher(doc)
    idioms = [match["idiom"] for match in results]
    assert "pure and simple" not in idioms


def test_shoot_em_up(idiomatcher):
    sent = "I think the advent of video games and third-person shoot 'em up games " \
           "did more for the zombie genre than a couple movies even."
    doc = idiomatcher.nlp(sent)
    results = idiomatcher(doc)
    idioms = [match["idiom"] for match in results]
    assert "shoot 'em up" in idioms


def test_beat_around_the_bush(idiomatcher):
    sent = "Just stop beating around the bush and tell me what the problem is!"
    doc = idiomatcher.nlp(sent)
    results = idiomatcher(doc)
    idioms = [match["idiom"] for match in results]
    assert "beat around the bush" in idioms


def test_have_blood_on_ones_hands(idiomatcher):
    sent = "Try running, you'll have blood on your hands."
    doc = idiomatcher.nlp(sent)
    results = idiomatcher(doc)
    idioms = [match["idiom"] for match in results]
    assert "have blood on one's hands" in idioms


def test_idioms_property(idiomatcher):
    idioms = ['catch-22', 'blow-by-blow', 'balls-out', 'come down to earth', 'this, that, and the other']
    for idiom in idioms:
        assert idiom in idiomatcher.idioms

    
def test_start_end(idiomatcher):
    sent = "what I know for sure is this. I can tell you that this is true"
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc)
    assert len(matches) == 1
    match = matches[0]
    logger.info(f"Match: {match}")
    assert doc[match['meta'][1]:match['meta'][2]].text == "I can tell you"


def  test_something_like_tp(idiomatcher):
    """
    something like - (informal, dated) A fine example or specimen of something
    """
    sent = "he had only to wish for it and it would come back to him. That is something like a whistle, thought Ashiepattle"
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc)
    assert len(matches) == 1
    match = matches[0]
    logger.info(f"Match: {match}")
    assert match['idiom'] == "something like"


def  test_something_like_tn(idiomatcher):
    """
    That's a specific phrase. something like. 
    """
    sent = "I think it's like one of those apple products."
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc)
    assert len(matches) == 0


def test_something_awful_tp(idiomatcher):
    """
    (degree, colloquial, idiomatic) Intensely or extremely; badly; in the worst way.
    """
    sent = "He wants to get out of there something awful, but he just doesn't have the money."
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc)
    assert len(matches) == 1
    match = matches[0]
    logger.info(f"Match: {match}")
    assert match['idiom'] == "something awful"



def test_something_awful_tn(idiomatcher):
    """
    something awful - (informal, dated) A very bad example or specimen of something
    """
    sent = "I'm not sure I'd want to be in the same room as that awful thing."
    doc = idiomatcher.nlp(sent)
    matches = idiomatcher(doc)
    assert len(matches) == 0
    
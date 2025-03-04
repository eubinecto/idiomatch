"""
Should include tests for the matcher.
"""
import pytest
import spacy
from typing import Optional, List
from spacy import Language
from idiomatch import Idiomatcher
from idiomatch.configs import NLP_MODEL


@pytest.fixture(scope="module")
def nlp():
    return spacy.load(NLP_MODEL)


@pytest.fixture(scope="module")
def idiomatcher(nlp):
    return Idiomatcher.from_pretrained(nlp)


def lemmatise(nlp, idiomatcher, sent: str) -> List[str]:
    doc = nlp(sent)
    matches = idiomatcher(doc)
    return [
        idiomatcher.vocab.strings[lemma_id]
        for (lemma_id, _, _) in matches
    ]


def test_identify_two_idioms(nlp, idiomatcher):
    sent = "Try running, you'll have blood on your hands."
    doc = nlp(sent)
    results = idiomatcher.identify(doc)
    # have blood on one's hands
    assert "have blood on one's hands" == results[0]['idiom']
    assert "have blood on your hands" == results[0]['span']
    assert idiomatcher(doc)[0] == results[0]['meta']
    # on one's hands
    assert "on one's hands" == results[1]['idiom']
    assert "on your hands" == results[1]['span']
    assert idiomatcher(doc)[1] == results[1]['meta']


def test_optional_hyphens(nlp, idiomatcher):
    # balls-out, balls out
    sent_balls = "in terms of rhyme, meter, and balls-out swagger."
    sent_balls_no_hyphens = "in terms of rhyme, meter, and balls out swagger."
    lemmas_catch = lemmatise(nlp, idiomatcher, sent_balls)
    lemmas_catch_no_hyphens = lemmatise(nlp, idiomatcher, sent_balls_no_hyphens)
    # blow-by-blow, blow by blow
    sent_blow = "he gave them a blow-by-blow account of your rescue"
    sent_blow_no_hyphens = "he gave them a blow by blow account of your rescue"
    lemmas_blow = lemmatise(nlp, idiomatcher, sent_blow)
    lemmas_blow_no_hyphens = lemmatise(nlp, idiomatcher, sent_blow_no_hyphens)
    assert "balls-out" in lemmas_catch
    assert "balls-out" in lemmas_catch_no_hyphens
    assert "blow-by-blow" in lemmas_blow
    assert "blow-by-blow" in lemmas_blow_no_hyphens


def test_noun_verb_inflection(nlp, idiomatcher):
    # teach someone a lesson
    sent_teach = "they were teaching me a lesson for daring to complain."
    # ahead of one's time
    sent_ahead = "Jo is a playwright who has always been ahead of her time"
    lemmas_teach = lemmatise(nlp, idiomatcher, sent_teach)
    lemmas_ahead = lemmatise(nlp, idiomatcher, sent_ahead)
    assert "teach someone a lesson" in lemmas_teach
    assert "ahead of one's time" in lemmas_ahead


# rigorously testing for hyphenated terms.
def test_match_catch_22(nlp, idiomatcher):
    # TODO: This does not pass.
    sent_1 = "qualities attributed to the drug. It is a catch-22 for any trainer or owner."
    matches = idiomatcher(nlp(sent_1))
    assert matches


def test_match_catch_22_no_hyphen(nlp, idiomatcher):
    sent_1 = "qualities attributed to the drug. It is a catch 22 for any trainer or owner."
    doc = nlp(sent_1)
    matches = idiomatcher(doc)
    assert matches


def test_match_catch_22_capitalised(nlp, idiomatcher):
    sent_1 = "qualities attributed to the drug. It is a Catch-22 for any trainer or owner."
    doc = nlp(sent_1)
    matches = idiomatcher(doc)
    assert matches


def test_match_blow_by_blow(nlp, idiomatcher):
    sent_1 = "He literally gives a blow-by-blow of how he killed her"
    matches = idiomatcher(nlp(sent_1))
    assert matches


def test_match_blow_by_blow_no_hyphen(nlp, idiomatcher):
    sent_1 = "He literally gives a blow by blow of how he killed her"
    matches = idiomatcher(nlp(sent_1))
    assert matches


def test_match_blow_by_blow_capitalised(nlp, idiomatcher):
    sent_1 = "He literally gives a Blow-By-Blow of how he killed her"
    # how should you fix this...?
    # we are doing exact match... at least for hyphenated terms.
    matches = idiomatcher(nlp(sent_1))
    assert matches


def test_balls_out(nlp, idiomatcher):
    sent_1 = " in terms of rhyme, meter, and balls-out swagger. "
    matches = idiomatcher(nlp(sent_1))
    assert matches


def test_balls_out_capitalised_one(nlp, idiomatcher):
    sent_1 = " in terms of rhyme, meter, and Balls-out swagger. "
    matches = idiomatcher(nlp(sent_1))
    assert matches


def test_balls_out_capitalised_two(nlp, idiomatcher):
    sent_1 = " in terms of rhyme, meter, and Balls-Out swagger. "
    matches = idiomatcher(nlp(sent_1))
    assert matches


def test_balls_out_no_hyphen(nlp, idiomatcher):
    sent_1 = " in terms of rhyme, meter, and balls out swagger. "
    matches = idiomatcher(nlp(sent_1))
    assert matches


def test_come_down_to_earth(nlp, idiomatcher):
    sent_1 = "Gosh, I must say perhaps we should um, sort of come down to earth" \
             " and sample some of this delightful food."
    lemmas = lemmatise(nlp, idiomatcher, sent_1)
    assert "come down to earth" in lemmas


def test_come_down_to_earth_capitalised(nlp, idiomatcher):
    sent_1 = "Gosh, I must say perhaps we should um, sort of come down to Earth" \
             " and sample some of this delightful food."
    lemmas = lemmatise(nlp, idiomatcher, sent_1)
    assert "come down to earth" in lemmas


def test_comma_optional(nlp, idiomatcher):
    sent = "Also, all those who believe that marriage makes people this that and the other" \
           " more than cohabitation is relying on OLD studies. "
    lemmas = lemmatise(nlp, idiomatcher, sent)
    assert "this, that, and the other" in lemmas


def test_and_not_optional(nlp, idiomatcher):
    sent = "... unable to conceive how a pure simple mind can exist without" \
           " any substance annexed to it."
    lemmas = lemmatise(nlp, idiomatcher, sent)
    assert "pure and simple" not in lemmas


def test_shoot_em_up(nlp, idiomatcher):
    sent = "I think the advent of video games and third-person shoot 'em up games " \
           "did more for the zombie genre than a couple movies even."
    lemmas = lemmatise(nlp, idiomatcher, sent)
    assert "shoot 'em up" in lemmas


def test_beat_around_the_bush(nlp, idiomatcher):
    sent = "Just stop beating around the bush and tell me what the problem is!"
    lemmas = lemmatise(nlp, idiomatcher, sent)
    assert "beat around the bush" in lemmas


def test_have_blood_on_ones_hands(nlp, idiomatcher):
    sent = "Try running, you'll have blood on your hands."
    lemmas = lemmatise(nlp, idiomatcher, sent)
    assert "have blood on one's hands" in lemmas

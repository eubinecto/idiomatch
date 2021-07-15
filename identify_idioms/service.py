from spacy import Language, Vocab
from spacy.matcher import Matcher
from identify_idioms.builders import IIPBuilder, IdiomMatcherBuilder


def build_iip() -> Language:
    """
    builds identify-idiom-pipeline. Built on top of web-core-sm.
    """
    iip_builder = IIPBuilder()
    return iip_builder.construct()


def build_idiom_matcher(vocab: Vocab) -> Matcher:
    """
    given a vocabulary, builds an idiom matcher.
    the idioms are added to the vocabulary.
    """
    idiom_matcher_builder = IdiomMatcherBuilder()
    return idiom_matcher_builder.construct(vocab)

from spacy import Language, Vocab
from spacy.matcher import Matcher
from identify_idioms import builders


def build_iip() -> Language:
    """
    builds identify-idiom-pipeline. Built on top of web-core-sm.
    """
    iip_builder = builders.IIPBuilder()
    return iip_builder.construct()


def build_idiom_matcher(vocab: Vocab) -> Matcher:
    """
    given a vocabulary, builds an idiom matcher.
    the idioms are added to the vocabulary.
    """
    idiom_matcher_builder = builders.IdiomMatcherBuilder()
    return idiom_matcher_builder.construct(vocab)

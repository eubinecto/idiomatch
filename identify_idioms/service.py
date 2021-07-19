from spacy import Vocab
from spacy.matcher import Matcher
from identify_idioms.builders import IdiomMatcherBuilder


def build_idiom_matcher(vocab: Vocab) -> Matcher:
    """
    given a vocabulary, builds an idiom matcher.
    the idioms are added to the vocabulary.
    """
    idiom_matcher_builder = IdiomMatcherBuilder()
    return idiom_matcher_builder.construct(vocab)

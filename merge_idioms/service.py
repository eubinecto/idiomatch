from spacy import Language, Vocab
from spacy.matcher import Matcher
from merge_idioms import builders


def build_mip() -> Language:
    """
    builds merge-idiom-pipeline. Built on top of
    """
    mip_builder = builders.MIPBuilder()
    return mip_builder.construct()


def build_idiom_matcher(vocab: Vocab) -> Matcher:
    """
    given a vocabulary, builds an idiom matcher.
    the idioms are added to the vocabulary.
    """
    idiom_matcher_builder = builders.IdiomMatcherBuilder()
    return idiom_matcher_builder.construct(vocab)

# TODO: add load_target_idioms

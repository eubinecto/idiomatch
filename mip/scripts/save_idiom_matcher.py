"""
this saves a Spacy's matcher for matching a fixed set of idioms.
"""
from spacy import load
import pickle
from builders import IdiomMatcherBuilder
from config import NLP_MODEL, IDIOM_MATCHER_PKL_PATH, SLIDE_TSV_PATH
from loaders import IdiomsLoader


def main():
    nlp = load(NLP_MODEL)
    # load idioms on to memory.
    idioms_loader = IdiomsLoader(path=SLIDE_TSV_PATH)
    idioms = idioms_loader.load(target_only=True)
    idiom_matcher_builder = IdiomMatcherBuilder(nlp, idioms)
    idiom_matcher_builder.construct()
    idiom_matcher = idiom_matcher_builder.idiom_matcher
    # save it as pickle binary. (matcher is not JSON-serializable.. this is the only way)
    with open(IDIOM_MATCHER_PKL_PATH, 'wb') as fh:
        fh.write(pickle.dumps(idiom_matcher))


if __name__ == '__main__':
    main()

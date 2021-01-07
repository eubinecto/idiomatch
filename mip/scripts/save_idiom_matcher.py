"""
this saves a Spacy's matcher for matching a fixed set of idioms.
"""
import pickle
from mip.builders import IdiomMatcherBuilder
from config import IDIOM_MATCHER_PKL_PATH


def main():
    idiom_matcher_builder = IdiomMatcherBuilder()
    idiom_matcher_builder.construct()
    # save it as pickle binary. (matcher is not JSON-serializable.. this is the only way)
    with open(IDIOM_MATCHER_PKL_PATH, 'wb') as fh:
        fh.write(pickle.dumps(idiom_matcher_builder.idiom_matcher))


if __name__ == '__main__':
    main()

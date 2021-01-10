import pickle

from spacy import load

from builders import IdiomMatcherBuilder
from config import NLP_MODEL_NAME, IDIOM_MATCHER_PKL_PATH


def main():
    idiom_matcher_builder = IdiomMatcherBuilder()
    nlp = load(NLP_MODEL_NAME)
    # use the default vocab of this model
    idiom_matcher_builder.construct(nlp.vocab)
    with open(IDIOM_MATCHER_PKL_PATH, 'wb') as fh:
        fh.write(pickle.dumps(idiom_matcher_builder.idiom_matcher))


if __name__ == '__main__':
    main()

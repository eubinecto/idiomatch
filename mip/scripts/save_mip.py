

from spacy import load
from config import NLP_MODEL, MIP_PKL_PATH
from loaders import IdiomMatcherLoader
from utils import MergeIdiomPipeline
import argparse
import pickle


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("idiom_matcher_pkl_path", type=str,
                        help="path to the pickle binary of idiom_matcher")
    args = parser.parse_args()
    matcher_path = args.idiom_matcher_pkl_path
    nlp = load(NLP_MODEL)
    idiom_matcher_loader = IdiomMatcherLoader(path=matcher_path)
    idiom_matcher = idiom_matcher_loader.load()
    mip = MergeIdiomPipeline(nlp, idiom_matcher)

    # ah.. come on. this actually works.
    with open(MIP_PKL_PATH, 'wb') as fh:
        fh.write(pickle.dumps(mip))


if __name__ == '__main__':
    main()

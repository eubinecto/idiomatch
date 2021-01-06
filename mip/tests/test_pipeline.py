from unittest import TestCase
import os
# use environment variable for passing paths to idiom_matcher
from spacy import load

from config import NLP_MODEL
from mip.loaders import IdiomMatcherLoader
from mip.pipeline import MergeIdiomPipeline

# to be accessed later.
os.environ['IDIOM_MATCHER_PKL_PATH'] = \
    "/Users/eubin/Desktop/Projects/Big/merge-idiom-pipeline/data/matcher/idiom_matcher_06_01_2021__17_23_02.pkl"


class TestMergeIdiomPipeline(TestCase):
    # prepare resource
    IDIOM_MATCHER_PKL_PATH = os.environ['IDIOM_MATCHER_PKL_PATH']
    idiom_matcher = IdiomMatcherLoader(IDIOM_MATCHER_PKL_PATH).load()
    nlp = load(NLP_MODEL)
    # this is the one to use.
    mip = MergeIdiomPipeline(nlp, idiom_matcher)


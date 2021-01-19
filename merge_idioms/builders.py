from typing import Generator, List, Callable, Optional
from spacy import Language, load, Vocab
from spacy.matcher import Matcher
from merge_idioms.config import NLP_MODEL_NAME, MIP_NAME, MIP_VERSION
from merge_idioms.loaders import TargetIdiomsLoader, IdiomPatternsLoader
from merge_idioms.cases import PRP_PLACEHOLDER_CASES, PRON_PLACEHOLDER_CASES
import logging
from sys import stdout
logging.basicConfig(stream=stdout, level=logging.INFO)  # why does logging not work?


class Builder:

    def construct(self, *args):
        for step in self.steps():
            step()

    def steps(self) -> List[Callable]:
        raise NotImplementedError

    def prepare(self, *args):
        raise NotImplementedError


class IdiomPatternsBuilder(Builder):

    def __init__(self):
        self.nlp: Optional[Language] = None
        self.target_idioms: Optional[Generator[str, None, None]] = None
        self.idiom_patterns: Optional[dict] = None  # to build

    def steps(self) -> List[Callable]:
        return [
            self.prepare,
            self.add_tok_special_cases,
            self.build_idiom_patterns
        ]

    def prepare(self, *args):
        self.nlp = load(NLP_MODEL_NAME)
        self.target_idioms = TargetIdiomsLoader().load()
        self.idiom_patterns = dict()

    def add_tok_special_cases(self):
        """
        the special cases.  (one's, someone's, catch-22.. etc)
        """
        self.nlp.add_pipe("add_special_cases", before="tok2vec")

    def build_idiom_patterns(self):
        # then add idiom matches
        logger = logging.getLogger("build_idiom_patterns")
        for idiom in self.target_idioms:
            idiom_doc = self.nlp(idiom)
            if "-" in idiom:  # hyphenated idioms
                pattern = [
                    {"TAG": "PRP$"} if token.text in PRP_PLACEHOLDER_CASES
                    # OP = ? - no occurrence or 1 occurrence
                    # https://spacy.io/usage/rule-based-matching#quantifiers
                    else {"TEXT": "-", "OP": "?"} if token.text == "-"
                    # don't use lemma (this is to avoid false-positives as much as I can)
                    # using regexp for case-insensitive match
                    # https://stackoverflow.com/a/42406605
                    else {"TEXT": {"REGEX": r"(?i)^{}$".format(token.text)}}
                    for token in idiom_doc
                ]  # include hyphens
                patterns = [pattern]
            else:  # non-hyphenated idioms
                pattern = [
                    {"TAG": "PRP$"} if token.text in PRP_PLACEHOLDER_CASES
                    else {"POS": "PRON"} if token.text in PRON_PLACEHOLDER_CASES
                    # some people may not use comma
                    else {"TEXT": token.text, "OP": "?"} if token.text == ","  # comma is optional
                    else {"TEXT": token.text, "OP": "?"} if token.text == "and"  # and is optional
                    else {"TEXT": token.text, "OP": "?"} if token.text in ("a", "an", "the")  # articles are optional
                    else {"LEMMA": {"REGEX": r"(?i)^{}$".format(token.lemma_)}}
                    for token in idiom_doc
                ]
                patterns = [pattern]
            # log each pattern
            logger.info(str(patterns))
            # build the patten
            self.idiom_patterns.update(
                {
                    # key = the str rep of idiom
                    # value = the patterns (list of list of dicts)
                    # as for the key, use the string as-is
                    idiom: patterns
                }
            )


class IdiomMatcherBuilder(Builder):

    def __init__(self):
        """
        given a language and a generator of idioms, this
        """
        self.vocab: Optional[Vocab] = None
        self.idiom_patterns: Optional[dict] = None
        self.idiom_matcher: Optional[Matcher] = None  # to be built

    def construct(self, vocab: Vocab):
        """
        must be given a vocab.
        :param vocab:
        :return:
        """
        self.vocab = vocab
        super(IdiomMatcherBuilder, self).construct()

    def steps(self) -> List[Callable]:
        # order matters. this is why I'm using a builder pattern.
        return [
            self.prepare,
            self.load_idiom_patterns,
            self.add_idiom_patterns
        ]

    def prepare(self):
        """
        prepare the ingredients needed
        """
        self.idiom_matcher = Matcher(self.vocab)

    def load_idiom_patterns(self):
        # build the patterns here.
        # well..
        self.idiom_patterns = IdiomPatternsLoader().load()

    def add_idiom_patterns(self):
        logger = logging.getLogger("add_idiom_patterns")
        logger.info("adding patterns into idiom_matcher...")
        for idiom, patterns in self.idiom_patterns.items():
            self.idiom_matcher.add(idiom, patterns)


class MIPBuilder(Builder):

    def __init__(self):
        self.mip: Optional[Language] = None

    def steps(self) -> List[Callable]:
        return [
            self.prepare,
            self.add_merge_idiom_comp,
            self.update_meta
        ]

    def prepare(self, *args):
        # nlp model is the base
        self.mip = load(NLP_MODEL_NAME)

    def add_merge_idiom_comp(self):
        # make sure the component is added at the end of the pipeline.
        # or, at least after tok2vec & lemmatizer
        self.mip.add_pipe("add_special_cases", first=True)
        self.mip.add_pipe("merge_idioms", last=True)

    def update_meta(self):
        # can I change the name & version of this pipeline?
        # you could later add description here.
        self.mip.meta['name'] += "_" + MIP_NAME
        self.mip.meta['version'] = MIP_VERSION

from typing import Generator, List, Callable, Optional
from spacy import Language, load, Vocab
from spacy.matcher import Matcher
from config import SLIDE_TSV_PATH, NLP_MODEL, IDIOM_PATTERNS_JSON_PATH
from loaders import IdiomsLoader, IdiomPatternsLoader
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
    # some cases
    POSS_HOLDER_CASES = {
        "one's": [{"ORTH": "one's"}],
        "someone's": [{"ORTH": "someone's"}]
    }
    # some cases that must be hard-coded.
    SPECIAL_IDIOM_CASES = {
        "catch-22": [{"ORTH": "catch"}, {"ORTH": "-"}, {"ORTH": "22"}]
    }

    def __init__(self):
        self.nlp: Optional[Language] = None
        self.idioms: Optional[Generator[str, None, None]] = None
        # this is the one to build
        self.idiom_patterns: Optional[dict] = None

    def steps(self) -> List[Callable]:
        return [
            self.prepare,
            self.build_tokenizer_patterns,
            self.build_idiom_patterns
        ]

    def prepare(self, *args):
        self.nlp = load(NLP_MODEL)
        idioms_loader = IdiomsLoader(path=SLIDE_TSV_PATH)
        self.idioms = idioms_loader.load(target_only=True)
        self.idiom_patterns = dict()

    def build_tokenizer_patterns(self):
        """
        hard-coding tokenisation rules.
        """
        # add cases for place holders
        for placeholder, case in self.POSS_HOLDER_CASES.items():
            self.nlp.tokenizer.add_special_case(placeholder, case)
        # add cases for words hyphenated with numbers
        for idiom, case in self.SPECIAL_IDIOM_CASES.items():
            self.nlp.tokenizer.add_special_case(idiom, case)

    def build_idiom_patterns(self):
        # then add idiom matches
        logger = logging.getLogger("build_idiom_patterns")
        for idiom in self.idioms:
            # for each idiom, you want to build this.
            # as for building patterns, use uncased version. of the idiom.
            # if you just want to tokenize strings, use
            # nlp.tokenizer.pipe()
            # https://stackoverflow.com/a/59615431
            # I'm not using it here because I need to access lemmas
            idiom_doc = self.nlp(idiom.lower())
            if "-" in idiom:
                # TODO: could change this to regexp?
                # should include both hyphenated & non-hyphenated forms
                # e.g. catch-22, catch 22
                pattern_hyphen = [
                    {"TAG": "PRP$"} if token.text in self.POSS_HOLDER_CASES.keys()
                    else {"ORTH": token.text}  # don't use lemma
                    for token in idiom_doc
                ]  # include hyphens
                pattern_no_hyphen = [
                    {"TAG": "PRP$"} if token.text in self.POSS_HOLDER_CASES.keys()
                    else {"ORTH": token.text}  # don't use lemma
                    for token in idiom_doc
                    if token.text != "-"
                ]
                patterns = [
                    # include two patterns
                    pattern_hyphen,
                    pattern_no_hyphen
                ]
            else:
                pattern = [
                    {"TAG": "PRP$"} if token.text in self.POSS_HOLDER_CASES.keys()
                    else {"LEMMA": token.lemma_}  # if not a verb, we do exact-match
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
            self.add_idiom_patterns
        ]

    def prepare(self):
        """
        prepare the ingredients needed
        """
        self.idiom_patterns = IdiomPatternsLoader(IDIOM_PATTERNS_JSON_PATH).load()
        self.idiom_matcher = Matcher(self.vocab)

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
            self.add_merge_idioms_component
        ]

    def prepare(self, *args):
        self.mip = load(NLP_MODEL)

    def add_merge_idioms_component(self):
        """
        the pipe must be added before.
        """
        self.mip.add_pipe("merge_idioms", after="lemmatizer")

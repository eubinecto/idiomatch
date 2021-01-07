from typing import Generator, List, Callable, Optional
from spacy import Language, load, Vocab
from spacy.matcher import Matcher
from config import SLIDE_TSV_PATH, NLP_MODEL, IDIOM_PATTERNS_JSON_PATH
from loaders import IdiomsLoader, IdiomPatternsLoader
import logging
from hardcoded import POSS_HOLDERS
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
        self.idioms: Optional[Generator[str, None, None]] = None
        # this is the one to build
        self.idiom_patterns: Optional[dict] = None

    def steps(self) -> List[Callable]:
        return [
            self.prepare,
            self.add_component_to_pipe,
            self.build_idiom_patterns
        ]

    def prepare(self, *args):
        self.nlp = load(NLP_MODEL)
        idioms_loader = IdiomsLoader(path=SLIDE_TSV_PATH)
        self.idioms = idioms_loader.load(target_only=True)
        self.idiom_patterns = dict()

    def add_component_to_pipe(self):
        """
        the special cases.
        """
        self.nlp.add_pipe("add_special_cases", before="tok2vec")

    def build_idiom_patterns(self):
        # then add idiom matches
        logger = logging.getLogger("build_idiom_patterns")
        for idiom in self.idioms:
            idiom_norm = idiom.lower()
            # for each idiom, you want to build this.
            # as for building patterns, use uncased version. of the idiom.
            # if you just want to tokenize strings, use
            # nlp.tokenizer.pipe()
            # https://stackoverflow.com/a/59615431
            # I'm not using it here because I need to access lemmas
            idiom_doc = self.nlp(idiom_norm)
            if "-" in idiom:
                # should include both hyphenated & non-hyphenated forms
                # e.g. catch-22, catch 22
                pattern = [
                    {"TAG": "PRP$"} if token.text in POSS_HOLDERS
                    # OP = ? - no occurrence or 1 occurrence
                    # https://spacy.io/usage/rule-based-matching#quantifiers
                    else {"ORTH": "-", "OP": "?"} if token.text == "-"
                    # don't use lemma (yeah..because they are not supposed to change)
                    # using regexp for case-insensitive match
                    # https://stackoverflow.com/a/42406605
                    else {"TEXT": {"REGEX": r"(?i){}".format(token.text)}}
                    for token in idiom_doc
                ]  # include hyphens

                patterns = [pattern]
            else:
                pattern = [
                    {"TAG": "PRP$"} if token.text in POSS_HOLDERS
                    # some people may not use comma
                    else {"LEMMA": token.lemma_, "OP": "?"} if token.text == ","
                    else {"LEMMA": token.lemma_}
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
                    idiom_norm: patterns
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
            self.add_components
        ]

    def prepare(self, *args):
        self.mip = load(NLP_MODEL)

    def add_components(self):
        self.mip.add_pipe("add_special_cases", before="tok2vec")
        self.mip.add_pipe("merge_idioms", after="lemmatizer")

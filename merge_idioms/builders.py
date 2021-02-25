from typing import List, Callable, Optional, Dict
from spacy import Language, load, Vocab
from spacy.matcher import Matcher
from spacy.tokens import Doc
from merge_idioms.config import BASE_NLP_MODEL, MIP_NAME, MIP_VERSION, TARGET_IDIOM_MIN_LENGTH, \
    TARGET_IDIOM_MIN_WORD_COUNT
from merge_idioms.loaders import IdiomPatternsLoader, IdiomAltsLoader, SlideIdiomAltsLoader
from merge_idioms.cases import PRP_PLACEHOLDER_CASES, PRON_PLACEHOLDER_CASES, OPTIONAL_CASES, IGNORED_CASES, \
    MORE_IDIOM_ALTS_CASES
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
        self.idiom_alts: Optional[Dict[str, list]] = None
        self.idiom_patterns: Optional[Dict[str, list]] = None  # to build

    def construct(self, *args) -> Dict[str, list]:
        super(IdiomPatternsBuilder, self).construct()
        return self.idiom_patterns

    def steps(self) -> List[Callable]:
        return [
            self.prepare,
            self.add_tok_special_cases,
            self.build_idiom_patterns
        ]

    def prepare(self, *args):
        self.nlp = load(BASE_NLP_MODEL)
        self.idiom_alts = IdiomAltsLoader().load()
        self.idiom_patterns = dict()

    def add_tok_special_cases(self):
        """
        the special cases.  (one's, someone's, catch-22.. etc)
        """
        self.nlp.add_pipe("add_special_cases", before="tok2vec")

    @classmethod
    def build_pattern_hyphenated(cls, hyphenated_idiom_doc: Doc) -> List[Dict]:
        return [
            {"TAG": "PRP$"} if token.text in PRP_PLACEHOLDER_CASES
            # OP = ? - no occurrence or 1 occurrence
            # https://spacy.io/usage/rule-based-matching#quantifiers
            else {"TEXT": token.text, "OP": "?"} if token.text == "-"
            # don't use lemma (this is to avoid false-positives as much as I can)
            # using regexp for case-insensitive match
            # https://stackoverflow.com/a/42406605
            else {"TEXT": {"REGEX": r"(?i)^{}$".format(token.text)}}
            for token in hyphenated_idiom_doc
        ]  # include hyphens

    @classmethod
    def build_pattern(cls, idiom_doc: Doc) -> List[Dict]:
        return [
            {"TAG": "PRP$"} if token.text in PRP_PLACEHOLDER_CASES  # one's, someone's
            else {"POS": "PRON"} if token.text in PRON_PLACEHOLDER_CASES  # someone.
            else {"TEXT": token.text, "OP": "?"} if token.text in OPTIONAL_CASES  # comma is optional
            else {"LEMMA": {"REGEX": r"(?i)^{}$".format(token.lemma_)}}
            for token in idiom_doc
        ]

    def build_idiom_patterns(self):
        # then add idiom matches
        for idiom, alts in self.idiom_alts.items():
            patterns = list()
            idiom_doc = self.nlp(idiom)
            if "-" in idiom:  # hyphenated idioms
                pattern = self.build_pattern_hyphenated(idiom_doc)
                patterns.append(pattern)
            else:  # non-hyphenated idioms
                pattern = self.build_pattern(idiom_doc)
                patterns.append(pattern)
            # add patterns for alternatives as well
            for alt in alts:
                alt_doc = self.nlp(alt)
                if "-" in alt:  # hyphenated idioms
                    pattern = self.build_pattern_hyphenated(alt_doc)
                    patterns.append(pattern)
                else:  # non-hyphenated idioms
                    pattern = self.build_pattern(alt_doc)
                    patterns.append(pattern)
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

    def construct(self, vocab: Vocab) -> Matcher:
        """
        must be given a vocab.
        :param vocab:
        :return:
        """
        self.vocab = vocab
        super(IdiomMatcherBuilder, self).construct()
        return self.idiom_matcher

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
            try:
                self.idiom_matcher.add(idiom, patterns)
            except Exception as e:
                print(idiom)
                print(patterns)
                raise e


class MIPBuilder(Builder):

    def __init__(self):
        self.mip: Optional[Language] = None

    def steps(self) -> List[Callable]:
        return [
            self.prepare,
            self.add_components,
            self.update_meta
        ]

    def construct(self, *args) -> Language:
        super(MIPBuilder, self).construct()
        return self.mip

    def prepare(self, *args):
        # nlp model is the base
        self.mip = load(BASE_NLP_MODEL)

    def add_components(self):
        # make sure the component is added at the end of the pipeline.
        # or, at least after tok2vec & lemmatizer
        self.mip.add_pipe("add_special_cases", first=True)
        self.mip.add_pipe("merge_idioms", last=True)

    def update_meta(self):
        # can I change the name & version of this pipeline?
        # you could later add description here.
        self.mip.meta['name'] += "_" + MIP_NAME
        self.mip.meta['version'] = MIP_VERSION


class IdiomAltsBuilder(Builder):
    def __init__(self):
        self.slide_idiom_alts_tsv_path: Optional[str] = None
        self.slide_idiom_alts: Optional[Dict[str, list]] = None
        self.idiom_alts: Optional[Dict[str, list]] = None

    def steps(self) -> List[Callable]:
        return [
            self.prepare,
            self.add_more_idiom_alts,
            self.build_idiom_alts
        ]
    
    def construct(self, slide_idiom_alts_tsv_path: str) -> Dict[str, list]:
        self.slide_idiom_alts_tsv_path = slide_idiom_alts_tsv_path
        super(IdiomAltsBuilder, self).construct()
        return self.idiom_alts
        
    def prepare(self):
        # prepare slide idioms with alternatives
        self.slide_idiom_alts = SlideIdiomAltsLoader(self.slide_idiom_alts_tsv_path).load()

    def add_more_idiom_alts(self):
        for idiom, alts in MORE_IDIOM_ALTS_CASES.items():
            if idiom in self.slide_idiom_alts:
                self.slide_idiom_alts[idiom] += alts
            else:
                self.slide_idiom_alts[idiom] = alts

    @staticmethod
    def norm_case(idiom: str) -> str:
        return idiom.lower() \
            .replace("i ", "I ") \
            .replace(" i ", " I ") \
            .replace("i'm", "I'm") \
            .replace("i'll", "I'll") \
            .replace("i\'d", "I'd")

    @staticmethod
    def is_target(idiom: str) -> bool:
        def above_min_word_count(idiom_: str) -> bool:
            return len(idiom_.split(" ")) >= TARGET_IDIOM_MIN_WORD_COUNT

        def above_min_length(idiom_: str) -> bool:
            return len(idiom_) >= TARGET_IDIOM_MIN_LENGTH

        def is_hyphenated(idiom_: str) -> bool:
            return "-" in idiom_

        return (idiom not in IGNORED_CASES)\
               and (above_min_word_count(idiom) or
                    above_min_length(idiom) or
                    is_hyphenated(idiom))
    
    def build_idiom_alts(self):
        self.idiom_alts = {
            self.norm_case(idiom): [self.norm_case(alt) for alt in alts]
            for idiom, alts in self.slide_idiom_alts.items()
            if self.is_target(idiom)
        }

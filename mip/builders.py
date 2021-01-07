import codecs
import pickle
from typing import Generator, List, Callable, Optional
from spacy import Language, load
from spacy.matcher import Matcher
from config import SLIDE_TSV_PATH, NLP_MODEL
from mip.component import MergeIdiomComponent
from mip.loaders import IdiomsLoader, IdiomMatcherLoader
import logging
from sys import stdout
logging.basicConfig(stream=stdout, level=logging.INFO)


class Builder:

    def construct(self, *args):
        for step in self.steps():
            step()

    def steps(self) -> List[Callable]:
        raise NotImplementedError

    def prepare(self, *args):
        raise NotImplementedError


class IdiomMatcherBuilder(Builder):
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
        """
        given a language and a generator of idioms, this
        """
        self.nlp: Optional[Language] = None
        self.idioms: Optional[Generator[str, None, None]] = None
        self.idiom_matcher: Optional[Matcher] = None

    def steps(self) -> List[Callable]:
        # order matters. this is why I'm using a builder pattern.
        return [
            self.prepare,
            self.build_tokenizer_patterns,
            self.build_idiom_patterns
        ]

    def prepare(self):
        """
        prepare the ingredients needed
        """
        self.nlp = load(NLP_MODEL)
        # load idioms on to memory.
        idioms_loader = IdiomsLoader(path=SLIDE_TSV_PATH)
        self.idioms = idioms_loader.load(target_only=True)
        # give it the entire vocab.
        self.idiom_matcher = Matcher(self.nlp.vocab)

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
        logger = logging.getLogger("build_tokenizer_patterns")
        for idiom in self.idioms:
            # for each idiom, you want to build this.
            patterns: List[List[dict]]
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
            logger.info(print(patterns))
            self.idiom_matcher.add(idiom, patterns)


class MIPBuilder(Builder):
    # any constants go here.
    FACTORY_NAME = "merge_idiom"

    def __init__(self):
        # this is to be built
        self.mip: Optional[Language] = None
        self.idiom_matcher_path: Optional[str] = None
        self.idiom_matcher: Optional[Matcher] = None
        self.idiom_matcher_str: Optional[str] = None
        
    def construct(self, idiom_matcher_pkl_path: str):
        self.idiom_matcher_path = idiom_matcher_pkl_path
        super(MIPBuilder, self).construct()

    def steps(self) -> List[Callable]:
        # remember, the order matters
        return [
            self.prepare,
            self.sync_vocab,
            self.pickle_idiom_matcher,
            self.register_factory,
            self.add_pipe
        ]

    def prepare(self):
        # load a pre-built idiom_matcher
        idiom_matcher_loader = IdiomMatcherLoader(self.idiom_matcher_path)
        self.idiom_matcher = idiom_matcher_loader.load()
        self.mip = load(NLP_MODEL)

    def sync_vocab(self):
        """
        idiom_matcher & the pipeline must share the same vocab.
        """
        self.mip.vocab = self.idiom_matcher.vocab

    def pickle_idiom_matcher(self):
        """
        # in order for this to be json-serializable, this must be in str type.
        # otherwise, ConfigParser will raise an exception.
        # https://stackoverflow.com/a/30469744
        """
        self.idiom_matcher_str = codecs.encode(
            pickle.dumps(self.idiom_matcher), "base64"
        ).decode()

    def register_factory(self):
        """
        # TODO - find the documentation for this.
        """
        Language.factory(
            name=MIPBuilder.FACTORY_NAME,
            retokenizes=True,  # we are merging, so it does retokenize
            default_config={"idiom_matcher_str": self.idiom_matcher_str},
            # the factory method.
            func=MergeIdiomComponent.create_merge_idiom_component
        )

    def add_pipe(self):
        """
        have to do this after lemmatization.
        """
        self.mip.add_pipe(MIPBuilder.FACTORY_NAME, after="lemmatizer")

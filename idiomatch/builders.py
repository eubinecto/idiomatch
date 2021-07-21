from abc import ABC
from typing import List, Callable, Optional, Dict
from spacy import Language
from spacy.tokens import Token
from tqdm import tqdm
from idiomatch.configs import \
    TARGET_IDIOM_MIN_LENGTH, \
    TARGET_IDIOM_MIN_WORD_COUNT, \
    SLOP, WILDCARD
from idiomatch.loaders import \
    load_slide_idioms
from idiomatch.cases import \
    IGNORED_CASES, \
    MORE_IDIOM_CASES, \
    PRP_PLACEHOLDER_CASES, \
    PRON_PLACEHOLDER_CASES, SPECIAL_TOK_CASES, OPTIONAL_CASES
import logging
from sys import stdout
import copy

logging.basicConfig(stream=stdout, level=logging.INFO)  # why does logging not work?


class Builder:

    def construct(self, *args):
        for step in self.steps():
            step()

    def steps(self) -> List[Callable]:
        raise NotImplementedError


class IdiomsBuilder(Builder):
    def __init__(self):
        self.slide_idioms: Optional[List[str]] = None
        self.idioms: Optional[List[str]] = None

    def steps(self) -> List[Callable]:
        return [
            self.prepare,
            self.add_more_idiom_cases,
            self.build_idioms,
        ]

    def construct(self) -> List[str]:
        super(IdiomsBuilder, self).construct()
        return self.idioms

    def prepare(self):
        # prepare slide idioms with alternatives
        self.slide_idioms = load_slide_idioms()

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

        return (idiom not in IGNORED_CASES) \
               and (above_min_word_count(idiom) or
                    above_min_length(idiom) or
                    is_hyphenated(idiom))

    def add_more_idiom_cases(self):
        self.slide_idioms += MORE_IDIOM_CASES

    def build_idioms(self):
        self.idioms = [
            self.norm_case(idiom)
            for idiom in self.slide_idioms
            if self.is_target(idiom)
        ]


class NLPBasedBuilder(Builder, ABC):

    def __init__(self, nlp: Language):
        self.nlp: Language = nlp
        self.add_special_tok_cases()

    def add_special_tok_cases(self):
        for term, case in SPECIAL_TOK_CASES.items():
            self.nlp.tokenizer.add_special_case(term, case)


class IdiomPatternsBuilder(NLPBasedBuilder):

    def __init__(self, nlp: Language):
        super().__init__(nlp)
        self.idioms: List[str] = list()
        self.idiom_patterns: Dict[str, list] = dict()  # this is the objective.

    def construct(self, idioms: List[str]) -> Dict[str, list]:
        self.idioms += idioms
        super(IdiomPatternsBuilder, self).construct()
        return copy.deepcopy(self.idiom_patterns)

    def steps(self) -> List[Callable]:
        return [
            self.build_patterns
        ]

    def clear(self):
        self.idioms.clear()
        self.idiom_patterns.clear()

    @staticmethod
    def insert_slop(patterns: List[dict], n: int) -> List[dict]:
        """
        getting use of implementation of intersperse, implemented in here.
        https://stackoverflow.com/a/5655780
        """
        slop_pattern = [{"TEXT": {"REGEX": WILDCARD}, "OP": "?"}] * n  # insert n number of slops.
        res = list()
        is_first = True
        for pattern in patterns:
            if not is_first:
                res += slop_pattern
            res.append(pattern)
            is_first = False
        return res

    @staticmethod
    def reorder(idiom_tokens: List[Token]) -> List[Token]:
        """
        if the pos of the first token is a verb, then reorder it such that the verb comes at the end.
        e.g. call someone's bluff -> someone's bluff call
        """
        tokens = [token for token in idiom_tokens]
        if tokens[0].pos_ == "VERB":
            first = tokens.pop(0)
            tokens.append(first)  # put the token at the end
        return tokens

    @classmethod
    def build_modification(cls, idiom_tokens: List[Token]) -> List[dict]:
        """
        slop
        """
        pattern = [
            {"TAG": "PRP$"} if token.text in PRP_PLACEHOLDER_CASES  # one's, someone's
            else {"POS": "PRON"} if token.text in PRON_PLACEHOLDER_CASES  # someone.
            else {"TEXT": token.text, "OP": "?"} if token.text in OPTIONAL_CASES
            else {"LEMMA": {"REGEX": r"(?i)^{}$".format(token.lemma_)}}
            for token in idiom_tokens
        ]
        # insert slop over the pattern
        return cls.insert_slop(pattern, SLOP)

    @classmethod
    def build_hyphenated(cls, idiom_tokens: List[Token]) -> List[dict]:
        pattern = [
            {"TEXT": token.text, "OP": "?"} if token.text == "-"
            # don't use lemma (this is to avoid false-positives as much as I can)
            # using regexp for case-insensitive match
            # https://stackoverflow.com/a/42406605
            else {"TEXT": {"REGEX": r"(?i)^{}$".format(token.text)}}
            for token in idiom_tokens
        ]
        # no openslot here.
        return pattern

    @classmethod
    def build_openslot(cls, idiom_tokens: List[Token]) -> List[dict]:
        """
        wildcard + slop
        """
        pattern = [
            # use a wildcard for placeholder cases.
            {"TEXT": {"REGEX": WILDCARD}} if token.text in (PRP_PLACEHOLDER_CASES + PRON_PLACEHOLDER_CASES)
            else {"TEXT": token.text, "OP": "?"} if token.text in OPTIONAL_CASES
            else {"LEMMA": {"REGEX": r"(?i)^{}$".format(token.lemma_)}}
            for token in idiom_tokens
        ]
        return cls.insert_slop(pattern, SLOP)

    @classmethod
    def build_passivisation_with_modification(cls, idiom_tokens: List[Token]) -> List[dict]:
        """
        reordering + slop
        """
        tokens = cls.reorder(idiom_tokens)
        return cls.build_modification(tokens)

    @classmethod
    def build_passivisation_with_openslot(cls, idiom_tokens: List[Token]) -> List[dict]:
        """
        reordering + wildcard + slop
        """
        tokens = cls.reorder(idiom_tokens)
        return cls.build_openslot(tokens)

    def build_patterns(self):
        # then add idiom matches
        for idiom in tqdm(self.idioms):
            idiom_tokens = [token for token in self.nlp(idiom)]
            # I just want to have all of them here, with a single line.
            patterns = [
                self.build_modification(idiom_tokens),
                self.build_openslot(idiom_tokens),
                self.build_hyphenated(idiom_tokens),
                self.build_passivisation_with_modification(idiom_tokens),
                self.build_passivisation_with_openslot(idiom_tokens)
            ]
            patterns = [pattern for pattern in patterns if pattern]  # filter out empty patterns.
            # then, update with these patterns.
            self.idiom_patterns.update(
                {
                    # key = the str rep of idiom
                    # value = the patterns (list of list of dicts)
                    idiom: patterns
                }
            )

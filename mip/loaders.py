import csv
import pickle
from typing import Generator, cast

from spacy.matcher import Matcher


class Loader:
    def __init__(self, path: str):
        self.path = path

    def load(self, *args, **kwargs):
        raise NotImplementedError


class IdiomsLoader(Loader):
    # not to include in the vocabulary
    IGNORED = (
        "if needs be"  # duplicate ->  "if need be" is enough.
    )

    CORRECTION_RULES = {
        # parenthesis is for when
        "have blood on one's hands": "have one's blood on one's hands"
    }

    DELIM = "\t"
    SEPARATOR = " "
    IDIOM_MIN_WC = 3  # aim for the idioms with length greater than 3
    IDIOM_MIN_LENGTH = 14

    def load(self, target_only: bool = True) -> Generator[str, None, None]:
        """

        :param target_only: if set to false, it will load all the idioms.
        :return:
        """
        corrected_idioms = (
            IdiomsLoader.correct_idiom(idiom)
            for idiom in self.idioms()
        )

        if target_only:
            return (
                idiom
                for idiom in corrected_idioms
                if self.is_target(idiom)
            )

        else:
            return corrected_idioms

    def idioms(self) -> Generator[str, None, None]:
        with open(self.path, 'r') as fh:
            slide_tsv = csv.reader(fh, delimiter="\t")
            # skip the  header
            next(slide_tsv)
            for row in slide_tsv:
                yield row[0]

    @classmethod
    def correct_idiom(cls, idiom: str) -> str:
        if idiom in cls.CORRECTION_RULES.keys():
            return cls.CORRECTION_RULES[idiom]
        else:
            return idiom

    @classmethod
    def is_above_min_len(cls, idiom: str) -> bool:
        return len(idiom) >= cls.IDIOM_MIN_LENGTH

    @classmethod
    def is_above_min_wc(cls, idiom: str) -> bool:
        return len(idiom.split(cls.SEPARATOR)) >= cls.IDIOM_MIN_WC

    @classmethod
    def is_hyphenated(cls, idiom: str) -> bool:
        return idiom.find("-") != -1

    @classmethod
    def is_not_ignored(cls, idiom: str) -> bool:
        return idiom not in cls.IGNORED

    @classmethod
    def is_target(cls, idiom: str) -> bool:
        # if it is either long enough or hyphenated, then I'm using it.
        return cls.is_not_ignored(idiom) and \
               (cls.is_above_min_wc(idiom) or
                cls.is_above_min_len(idiom) or
                cls.is_hyphenated(idiom))


class PklLoader(Loader):
    def load(self) -> object:
        with open(self.path, 'rb') as fh:
            return pickle.loads(fh.read())


class IdiomMatcherLoader(PklLoader):
    def load(self) -> Matcher:
        # need a type cast
        matcher = super(IdiomMatcherLoader, self).load()
        # just to avoid warning in IDE
        return cast(Matcher, matcher)

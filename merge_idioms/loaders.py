import csv
import json
from typing import Generator, Dict, List
from merge_idioms.cases import IGNORED_CASES, MORE_CASES
from merge_idioms.config import TARGET_IDIOMS_TXT_PATH, IDIOM_PATTERNS_JSON_PATH


class Loader:
    def load(self, *args, **kwargs):
        raise NotImplementedError


class IdiomsLoader(Loader):
    # not to include in the vocabulary
    SEPARATOR = " "
    # the settings for target idioms
    MIN_WC = 3  # aim for the idioms with length greater than 3
    MIN_LENGTH = 14  # aim for the idioms

    def __init__(self, slide_tsv_path: str):
        self.slide_tsv_path = slide_tsv_path

    def load(self, target_only: bool = True) -> Generator[str, None, None]:
        """

        :param target_only: if set to false, it will load all the idioms.
        :return:
        """
        to_return = self.idioms()
        if target_only:
            to_return = (
                idiom
                for idiom in to_return
                if self.is_target(idiom)
            )

        return (
            # case normalisation is done for all idioms
            self.lower_and_correct(idiom)
            for idiom in to_return
        )

    def idioms(self) -> List[str]:
        # manually added
        with open(self.slide_tsv_path, 'r') as fh:
            slide_tsv = csv.reader(fh, delimiter="\t")
            # skip the  header
            next(slide_tsv)
            idioms = [
                row[0]
                for row in slide_tsv
            ]
        for more_idiom in MORE_CASES:
            idioms.append(more_idiom)
        return idioms

    @classmethod
    def lower_and_correct(cls, idiom: str) -> str:
        return idiom.lower() \
                    .replace("i ", "I ") \
                    .replace(" i ", " I ") \
                    .replace("i'm", "I'm") \
                    .replace("i'll", "I'll") \
                    .replace("i\'d", "I'd")

    @classmethod
    def is_above_min_len(cls, idiom: str) -> bool:
        return len(idiom) >= cls.MIN_LENGTH

    @classmethod
    def is_above_min_wc(cls, idiom: str) -> bool:
        return len(idiom.split(cls.SEPARATOR)) >= cls.MIN_WC

    @classmethod
    def is_hyphenated(cls, idiom: str) -> bool:
        return idiom.find("-") != -1

    @classmethod
    def is_not_ignored(cls, idiom: str) -> bool:
        return idiom not in IGNORED_CASES

    @classmethod
    def is_target(cls, idiom: str) -> bool:
        # if it is either long enough or hyphenated, then I'm using it.
        return cls.is_not_ignored(idiom) and \
               (cls.is_above_min_wc(idiom) or
                cls.is_above_min_len(idiom) or
                cls.is_hyphenated(idiom))


class TargetIdiomsLoader(Loader):
    def __init__(self):
        self.target_idioms_txt_path = TARGET_IDIOMS_TXT_PATH

    def load(self, *args, **kwargs) -> Generator[str, None, None]:
        with open(TARGET_IDIOMS_TXT_PATH, 'r') as fh:
            for line in fh:
                yield line.strip()


class IdiomPatternsLoader(Loader):

    def __init__(self):
        self.idiom_patterns_json_path = IDIOM_PATTERNS_JSON_PATH

    def load(self, *args, **kwargs) -> Dict[str, list]:
        with open(self.idiom_patterns_json_path, 'r') as fh:
            return json.loads(fh.read())

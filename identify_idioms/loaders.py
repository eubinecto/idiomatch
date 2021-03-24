import csv
import json
from typing import List, Dict
from identify_idioms.config import IDIOM_PATTERNS_TSV, IDIOM_ALTS_TSV


class Loader:
    def load(self, *args, **kwargs):
        raise NotImplementedError


class SlideIdiomsLoader(Loader):
    def __init__(self, slide_tsv_path: str):
        self.slide_tsv_path = slide_tsv_path

    def load(self) -> List[str]:
        # manually added
        with open(self.slide_tsv_path, 'r') as fh:
            slide_tsv = csv.reader(fh, delimiter="\t")
            # skip the  header
            next(slide_tsv)
            return [
                row[0]
                for row in slide_tsv
            ]


class SlideIdiomAltsLoader(Loader):
    def __init__(self, slide_idiom_alts_tsv_path: str):
        self.slide_idiom_alts_tsv_path = slide_idiom_alts_tsv_path

    def load(self, *args, **kwargs) -> Dict[str, list]:
        with open(self.slide_idiom_alts_tsv_path, 'r') as fh:
            tsv_reader = csv.reader(fh, delimiter="\t")
            next(tsv_reader)
            return {
                row[0]: json.loads(row[1])
                for row in tsv_reader
            }


# belows return generators. (as no modification is needed)
class IdiomPatternsLoader(Loader):
    def load(self, *args, **kwargs) -> Dict[str, list]:
        with open(IDIOM_PATTERNS_TSV, 'r') as fh:
            tsv_reader = csv.reader(fh, delimiter="\t")
            next(tsv_reader)  # skip the header
            return {
                row[0]: json.loads(row[1])
                for row in tsv_reader
            }


class IdiomAltsLoader(Loader):
    def load(self, *args, **kwargs) -> Dict[str, list]:
        with open(IDIOM_ALTS_TSV, 'r') as fh:
            tsv_reader = csv.reader(fh, delimiter="\t")
            next(tsv_reader)  # skip the header
            return {
                row[0]: json.loads(row[1])
                for row in tsv_reader
            }

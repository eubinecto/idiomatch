import csv
import json
from typing import List, Dict
from idiomatch.paths import \
    SLIDE_TSV,\
    IDIOM_PATTERNS_TSV,\
    IDIOMS_TXT


def load_slide_idioms() -> List[str]:
    with open(SLIDE_TSV, 'r') as fh:
        slide_tsv = csv.reader(fh, delimiter="\t")
        # skip the  header
        next(slide_tsv)
        return [
            row[0]
            for row in slide_tsv
        ]


def load_idioms() -> List[str]:
    with open(IDIOMS_TXT, 'r') as fh:
        return [
            idiom.strip()
            for idiom in fh
        ]


def load_idiom_patterns() -> Dict[str, list]:
    with open(IDIOM_PATTERNS_TSV, 'r') as fh:
        tsv_reader = csv.reader(fh, delimiter="\t")
        next(tsv_reader)  # skip the header
        return {
            row[0]: json.loads(row[1])
            for row in tsv_reader
        }

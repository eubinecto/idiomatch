import csv
import json
import logging
from sys import stdout
import spacy
from identify_idioms.builders import IdiomPatternsBuilder
from identify_idioms.configs import NLP_MODEL
from identify_idioms.loaders import load_idioms
from identify_idioms.paths import IDIOM_PATTERNS_TSV

logging.basicConfig(stream=stdout, level=logging.INFO)


def main():
    # save the idiom_patterns
    idioms = load_idioms()
    nlp = spacy.load(NLP_MODEL)
    idiom_patterns = IdiomPatternsBuilder(nlp).construct(idioms)
    # just save it as a tsv file. - to be loaded later
    with open(IDIOM_PATTERNS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        # write the header
        tsv_writer.writerow(['idiom', 'patterns'])
        # write the rows
        for idiom, patterns in idiom_patterns.items():
            tsv_writer.writerow([idiom, json.dumps(patterns)])


if __name__ == '__main__':
    main()

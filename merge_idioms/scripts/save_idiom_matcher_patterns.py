import csv
import json
import logging
from sys import stdout
from config import IDIOM_MATCHER_PATTERNS_CSV_PATH
from loaders import IdiomMatcherLoader
logging.basicConfig(stream=stdout, level=logging.INFO)


def main():
    # save the idiom_patterns
    idiom_matcher = IdiomMatcherLoader().load()
    # then.. save them in csv.
    with open(IDIOM_MATCHER_PATTERNS_CSV_PATH, 'w') as fh:
        csv_writer = csv.writer(fh)
        # write the header
        csv_writer.writerow(['idiom', 'patterns'])
        # write the rows
        for idiom_lemma_id, patterns in idiom_matcher._patterns.items():
            idiom_lemma = idiom_matcher.vocab.strings[idiom_lemma_id]
            csv_writer.writerow([idiom_lemma, json.dumps(patterns)])


if __name__ == '__main__':
    main()

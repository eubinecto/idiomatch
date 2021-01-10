import csv
import json
import logging
from sys import stdout
from builders import IdiomPatternsBuilder
from config import IDIOM_PATTERNS_CSV_PATH, IDIOM_PATTERNS_JSON_PATH
logging.basicConfig(stream=stdout, level=logging.INFO)


def main():
    # save the idiom_patterns
    idiom_patterns_builder = IdiomPatternsBuilder()
    idiom_patterns_builder.construct()
    idiom_patterns = idiom_patterns_builder.idiom_patterns

    # save it as json
    with open(IDIOM_PATTERNS_JSON_PATH, 'w') as fh:
        fh.write(json.dumps(idiom_patterns))

    # then.. save them in csv.
    with open(IDIOM_PATTERNS_CSV_PATH, 'w') as fh:
        csv_writer = csv.writer(fh)
        # write the header
        csv_writer.writerow(['idiom', 'patterns'])
        # write the rows
        for idiom_lemma, patterns in idiom_patterns.items():
            csv_writer.writerow([idiom_lemma, json.dumps(patterns)])


if __name__ == '__main__':
    main()

import csv
import json
import logging
from sys import stdout
from config import IDIOM_PATTERNS_CSV_PATH, IDIOM_PATTERNS_JSON_PATH
from loaders import IdiomPatternsLoader

logging.basicConfig(stream=stdout, level=logging.INFO)


def main():
    idiom_patterns = IdiomPatternsLoader(IDIOM_PATTERNS_JSON_PATH).load()

    with open(IDIOM_PATTERNS_CSV_PATH, 'w') as fh:
        csv_writer = csv.writer(fh)
        # write the header
        csv_writer.writerow(['idiom', 'patterns'])
        # write the rows
        for idiom, patterns in idiom_patterns.items():
            csv_writer.writerow([idiom, json.dumps(patterns)])


if __name__ == '__main__':
    main()

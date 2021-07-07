import json
from identify_idioms.builders import IdiomAltsBuilder
from identify_idioms.paths import SLIDE_IDIOM_ALTS_TSV, IDIOM_ALTS_TSV
import csv


def main():
    idiom_alts = IdiomAltsBuilder().construct(SLIDE_IDIOM_ALTS_TSV)
    with open(IDIOM_ALTS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        schema = ["idiom", "alts"]
        tsv_writer.writerow(schema)
        for idiom, alts in idiom_alts.items():
            to_write = [idiom, json.dumps(alts)]
            tsv_writer.writerow(to_write)


if __name__ == '__main__':
    main()

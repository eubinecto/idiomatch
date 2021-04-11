import json
from requests import HTTPError
from identify_idioms.builders import IdiomAltsBuilder
from identify_idioms.loaders import SlideIdiomsLoader
from identify_idioms.config import SLIDE_TSV, SLIDE_IDIOM_ALTS_TSV
import csv
from os import path


def main():
    if path.exists(SLIDE_IDIOM_ALTS_TSV):
        raise ValueError("path already exists")

    alts_builder = IdiomAltsBuilder()
    with open(SLIDE_IDIOM_ALTS_TSV, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter="\t")
        schema = ['slide_idiom', 'alts']
        tsv_writer.writerow(schema)
        idioms = SlideIdiomsLoader(SLIDE_TSV).load()
        for idx, idiom in enumerate(idioms):
            try:
                alts = alts_builder.construct(idiom)
            except HTTPError as he:
                print(he)
                print("pass:" + idiom)
                continue
            else:
                to_write = [idiom, json.dumps(alts)]
                print(idx, to_write)
            tsv_writer.writerow(to_write)


if __name__ == '__main__':
    main()

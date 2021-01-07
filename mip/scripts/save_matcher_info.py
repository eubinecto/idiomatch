"""
this is just so that I can always see the pattern matching rules inside idiom matcher.
"""
import csv
from config import DELIM, IDIOM_MATCHER_INFO_TSV_PATH, IDIOM_MATCHER_PKL_CURR_PATH
import json
from mip.loaders import IdiomMatcherLoader


def main():
    # load idiom matcher from cache.
    idiom_matcher_loader = IdiomMatcherLoader(path=IDIOM_MATCHER_PKL_CURR_PATH)
    idiom_matcher = idiom_matcher_loader.load()
    with open(IDIOM_MATCHER_INFO_TSV_PATH, 'w') as fh:
        tsv_writer = csv.writer(fh, delimiter=DELIM)
        # write the header
        tsv_writer.writerow(['vocab_id', 'idiom', 'pattern'])
        # write the patterns
        # this is how you view the rules
        for vocab_id, pattern in idiom_matcher._patterns.items():
            idiom = idiom_matcher.vocab.strings[vocab_id]
            # as for the patterns, serialise it into json strings,
            # so that you can later use them if needed
            tsv_writer.writerow([vocab_id, idiom, json.dumps(pattern)])


if __name__ == '__main__':
    main()

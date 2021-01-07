"""
this saves a Spacy's matcher for matching a fixed set of idioms.
"""
import json
from builders import IdiomPatternsBuilder
from config import IDIOM_PATTERNS_JSON_PATH


def main():
    idiom_patterns_builder = IdiomPatternsBuilder()
    idiom_patterns_builder.construct()
    with open(IDIOM_PATTERNS_JSON_PATH, 'w') as fh:
        fh.write(json.dumps(idiom_patterns_builder.idiom_patterns))


if __name__ == '__main__':
    main()

"""
this saves a Spacy's matcher for matching a fixed set of idioms.
"""

from typing import List, Generator
from spacy import load, Language
from spacy.matcher import Matcher
import pickle
from config import NLP_MODEL, IDIOM_MATCHER_PKL_PATH
from utils import load_target_idioms


# I could amalgamate this into enum classes, I think.
# placeholder's for possessive pronouns should not be tokenized
POSS_HOLDER_CASES = {
    "one's": [{"ORTH": "one's"}],
    "someone's": [{"ORTH": "someone's"}]
}

# some cases that must be hard-coded.
SPECIAL_IDIOM_CASES = {
    "catch-22": [{"ORTH": "catch"}, {"ORTH": "-"}, {"ORTH": "22"}]
}


def build_idiom_matcher(nlp: Language, idioms: Generator[str, None, None]) -> Matcher:
    """
    uses nlp to build patterns for the matcher.
    """
    global POSS_HOLDER_CASES
    matcher = Matcher(nlp.vocab)  # matcher to build
    # then add idiom matches
    for idiom in idioms:
        # for each idiom, you want to build this.
        patterns: List[List[dict]]
        idiom_doc = nlp(idiom.lower())  # as for building patterns, use uncased version. of the idiom.
        if "-" in idiom:
            # should include both hyphenated & non-hyphenated forms
            # e.g. catch-22, catch 22
            pattern_hyphen = [
                {"TAG": "PRP$"} if token.text in POSS_HOLDER_CASES.keys()
                else {"ORTH": token.text}  # don't use lemma
                for token in idiom_doc
            ]  # include hyphens
            pattern_no_hyphen = [
                {"TAG": "PRP$"} if token.text in POSS_HOLDER_CASES.keys()
                else {"ORTH": token.text}  # don't use lemma
                for token in idiom_doc
                if token.text != "-"
            ]
            patterns = [
                # include two patterns
                pattern_hyphen,
                pattern_no_hyphen
            ]
        else:
            pattern = [
                {"TAG": "PRP$"} if token.text in POSS_HOLDER_CASES.keys()
                else {"LEMMA": token.lemma_}  # if not a verb, we do exact-match
                for token in idiom_doc
            ]
            patterns = [pattern]
        print(patterns)
        matcher.add(idiom, patterns)
    else:
        return matcher


def main():
    global POSS_HOLDER_CASES, SPECIAL_IDIOM_CASES
    # this is the end goal
    # load idioms on to memory.
    idioms = load_target_idioms()
    nlp = load(NLP_MODEL)
    # add cases for place holders
    for placeholder, case in POSS_HOLDER_CASES.items():
        nlp.tokenizer.add_special_case(placeholder, case)
    # add cases for words hyphenated with numbers
    for idiom, case in SPECIAL_IDIOM_CASES.items():
        nlp.tokenizer.add_special_case(idiom, case)
    # build patterns for the idioms into a matcher
    idiom_matcher = build_idiom_matcher(nlp, idioms)
    # save it as pickle binary. (matcher is not JSON-serializable.. this is the only way)
    with open(IDIOM_MATCHER_PKL_PATH, 'wb') as fh:
        fh.write(pickle.dumps(idiom_matcher))


if __name__ == '__main__':
    main()

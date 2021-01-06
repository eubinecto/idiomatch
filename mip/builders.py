from typing import Generator, List, Callable

from spacy import Language
from spacy.matcher import Matcher


class IdiomMatcherBuilder:
    # some cases
    POSS_HOLDER_CASES = {
        "one's": [{"ORTH": "one's"}],
        "someone's": [{"ORTH": "someone's"}]
    }
    # some cases that must be hard-coded.
    SPECIAL_IDIOM_CASES = {
        "catch-22": [{"ORTH": "catch"}, {"ORTH": "-"}, {"ORTH": "22"}]
    }

    def __init__(self, nlp: Language, idioms: Generator[str, None, None]):
        """
        given a language and a generator of idioms, this
        :param nlp:
        :param idioms:
        """
        self.nlp = nlp
        self.idiom_matcher = Matcher(nlp.vocab)
        self.idioms = idioms

    def construct(self):
        for step in self.steps():
            step()

    def steps(self) -> List[Callable]:
        # order matters. this is why I'm using a builder pattern.
        return [
            self.build_tokenizer_patterns,
            self.build_idiom_patterns
        ]

    def build_tokenizer_patterns(self):
        # add cases for place holders
        for placeholder, case in self.POSS_HOLDER_CASES.items():
            self.nlp.tokenizer.add_special_case(placeholder, case)
        # add cases for words hyphenated with numbers
        for idiom, case in self.SPECIAL_IDIOM_CASES.items():
            self.nlp.tokenizer.add_special_case(idiom, case)

    def build_idiom_patterns(self):
        # then add idiom matches
        for idiom in self.idioms:
            # for each idiom, you want to build this.
            patterns: List[List[dict]]
            idiom_doc = self.nlp(idiom.lower())  # as for building patterns, use uncased version. of the idiom.
            if "-" in idiom:
                # should include both hyphenated & non-hyphenated forms
                # e.g. catch-22, catch 22
                pattern_hyphen = [
                    {"TAG": "PRP$"} if token.text in self.POSS_HOLDER_CASES.keys()
                    else {"ORTH": token.text}  # don't use lemma
                    for token in idiom_doc
                ]  # include hyphens
                pattern_no_hyphen = [
                    {"TAG": "PRP$"} if token.text in self.POSS_HOLDER_CASES.keys()
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
                    {"TAG": "PRP$"} if token.text in self.POSS_HOLDER_CASES.keys()
                    else {"LEMMA": token.lemma_}  # if not a verb, we do exact-match
                    for token in idiom_doc
                ]
                patterns = [pattern]
            print(patterns)
            self.idiom_matcher.add(idiom, patterns)

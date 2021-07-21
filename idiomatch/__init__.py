# this is run whenever the module (merge_idioms) is imported.
# refer to this https://packaging.python.org/guides/single-sourcing-package-version/
from spacy import Language
from spacy.matcher.matcher import Matcher
from typing import List, Dict

from spacy.tokens.doc import Doc
from tqdm import tqdm
from idiomatch.builders import IdiomPatternsBuilder, NLPBasedBuilder
from idiomatch.loaders import load_idiom_patterns


class Idiomatcher(Matcher):
    """
    a matcher class for.. matching idioms.
    """
    def __init__(self, nlp: Language):
        super().__init__(nlp.vocab)  # give it the vocab
        self.idiom_patterns_builder = IdiomPatternsBuilder(nlp)

    @staticmethod
    def from_pretrained(nlp: Language) -> 'Idiomatcher':
        """
        load a pre-trained idiom matcher, which can identify more than 2000 English idioms.
        """

        idiom_matcher = Idiomatcher(nlp)
        idiom_patterns = load_idiom_patterns()
        idiom_matcher.add_idiom_patterns(idiom_patterns)
        return idiom_matcher

    def identify(self, doc: Doc) -> List[dict]:
        matches = self(doc)
        res = [
            {
                "idiom": self.idiom_patterns_builder.nlp.vocab.strings[token_id],
                "span": " ".join([token.text for token in doc[start:end]]),
                "meta": (token_id, start, end),
            }
            for token_id, start, end in matches
        ]
        return res

    def add_idiom_patterns(self, idiom_patterns: Dict[str, list]):
        for idiom, patterns in tqdm(idiom_patterns.items(),
                                    desc="adding patterns into idiomatcher..."):
            self.add(idiom, patterns)

    def add_idioms(self, idioms: List[str]):
        """
        Build patterns for the given idiom and add the patterns into the matcher.
        """
        # build patterns here.
        idiom_patterns = self.idiom_patterns_builder.construct(idioms)
        self.add_idiom_patterns(idiom_patterns)
        # clear the patterns at the end
        self.idiom_patterns_builder.clear()

from pathlib import Path
from langcodes import Language
from spacy.matcher.matcher import Matcher
from spacy.vocab import Vocab
from spacy.tokens.doc import Doc
from tqdm import tqdm
from pathlib import Path
from loguru import logger
from idiomatch.builders import build_idiom_patterns


class Idiomatcher(Matcher):
    """Language
    a matcher class for.. matching idioms.
    """

    @staticmethod
    def from_pretrained(vocab: Vocab) -> 'Idiomatcher':
        """
        load a pre-trained idiom matcher, which can identify more than 2000 English idioms.
        """
        logger.info("Loading pre-trained idiom matcher...")
        # load idiom patterns 
        import json
        patterns_path = Path(__file__).parent / "patterns.json"
        with open(patterns_path) as f:
            patterns = json.load(f)
        matcher = Idiomatcher(vocab)
        matcher.add_idiom_patterns(patterns)
        return matcher
        
    def __call__(self, doc: Doc) -> list[dict]:
        matches = super().__call__(doc)
        results = [
            {
                "idiom": self.vocab.strings[token_id],
                "span": " ".join([token.text for token in doc[start:end]]),
                "meta": (token_id, start, end),
            }
            for token_id, start, end in matches
        ]
        return results

    def add_idiom_patterns(self, patterns: dict[str, list]):
        for idiom, patterns in tqdm(patterns.items(),
                                    desc="adding patterns"):
            self.add(idiom, patterns)


    def add_idioms(self, nlp: Language, idioms: list[str]):
        """
        Build patterns for the given idiom and add the patterns into the matcher.
        """
        # build patterns here.
        patterns = build_idiom_patterns(idioms, nlp)
        self.add_idiom_patterns(patterns)

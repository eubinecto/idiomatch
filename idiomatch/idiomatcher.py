from pathlib import Path
from langcodes import Language
from spacy.matcher.matcher import Matcher
from spacy.tokens.doc import Doc
from spacy import Language
from tqdm import tqdm
import spacy
from pathlib import Path
from loguru import logger
from .builders import build
from .configs import NLP_MODEL
from .builders import add_special_tok_cases


class Idiomatcher(Matcher):
    """Language
    a matcher class for.. matching idioms.
    """

    def __init__(self, nlp: Language, n: int):
        super().__init__(nlp.vocab)
        # we must maintain an nlp model here
        self.nlp = nlp
        self.n = n  # slop val

    @property
    def idioms(self) -> list[str]:
        """Get all idioms that have been added to the matcher."""
        return [self.vocab.strings[key] for key in self._patterns.keys()]

    @staticmethod
    def from_pretrained(n: int = 1) -> 'Idiomatcher':
        """
        Load a pre-trained idiom matcher, which can identify more than 2000 English idioms.
        
        Args:
            slop: The slop value to use (1-5). If None, use the default from configs.SLOP
                  This determines which pattern file to load.
        Returns:
            An initialized Idiomatcher
        Raises:
            ValueError: If slop value is not in the range [1,5]
        """
        # Validate slop value
        if n < 1 or n > 5:   
            raise ValueError(f"Slop value must be between 1 and 5, got {n}")
        
        logger.info(f"Loading an nlp model to use with the matcher ({NLP_MODEL})...")
        try:
            # must be done for cases like catch-22
            nlp = spacy.load(NLP_MODEL)
            add_special_tok_cases(nlp)
        except OSError:
            raise OSError(
                f"Could not find the spaCy model '{NLP_MODEL}'. "
                "Please download it first by running:\n"
                f"python -m spacy download {NLP_MODEL}"
            )

        logger.info(f"Loading patterns with SLOP={n}...")
        # Determine which pattern file to load
        import json
        patterns_path = Path(__file__).parent / "patterns" / f"slop_{n}.json"
            
        if not patterns_path.exists():
            raise FileNotFoundError(f"Pattern file not found: {patterns_path}. Make sure to run the build_patterns.py script first.")
            
        with open(patterns_path) as f:
            patterns = json.load(f)
        matcher = Idiomatcher(nlp, n)
        for idiom, patterns in tqdm(patterns.items(),
                                    desc="adding patterns"):
            matcher.add(idiom, patterns)
        return matcher
        
    def __call__(self, doc: Doc, greedy: bool = True) -> list[dict]:
        matches = super().__call__(doc)
        results = [
            {
                "idiom": self.vocab.strings[token_id],
                "span": " ".join([token.text for token in doc[start:end]]),
                "meta": (token_id, start, end),
            }
            for token_id, start, end in matches
        ]
        
        if greedy and results:
            # Sort matches by span length (descending)
            # This prioritizes longer matches, which is what we want for greedy matching
            results.sort(key=lambda x: (x['meta'][2] - x['meta'][1]), reverse=True)
            
            # Keep track of non-contained matches
            new = []
            # Add the longest match first
            new.append(results[0])
            # For each remaining match, check if it's contained in any accepted match
            for match in results[1:]:
                start, end = match['meta'][1], match['meta'][2]
                is_contained = any(
                    start >= f_match['meta'][1] and end <= f_match['meta'][2]
                    for f_match in new
                )
                if not is_contained:
                    new.append(match)
            return new
        return results
        

    def add_idioms(self, idioms: list[str]):
        """
        Build patterns for the given idiom and add them into the matcher.
        """
        # build patterns here.
        patterns = build(idioms, self.nlp, self.n)
        for idiom, patterns in tqdm(patterns.items(),
                                    desc="adding patterns"):
            super().add(idiom, patterns)


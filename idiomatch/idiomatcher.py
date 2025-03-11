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

    @property
    def idioms(self) -> list[str]:
        """Get all idioms that have been added to the matcher."""
        return [self.vocab.strings[key] for key in self._patterns.keys()]

    @staticmethod
    def from_pretrained(vocab: Vocab, slop: int = 3) -> 'Idiomatcher':
        """
        Load a pre-trained idiom matcher, which can identify more than 2000 English idioms.
        
        Args:
            vocab: spaCy vocabulary
            slop: The slop value to use (1-5). If None, use the default from configs.SLOP
                  This determines which pattern file to load.
        
        Returns:
            An initialized Idiomatcher
            
        Raises:
            ValueError: If slop value is not in the range [1,5]
        """
        # Validate slop value
        if slop < 1 or slop > 5:   
            raise ValueError(f"Slop value must be between 1 and 5, got {slop}")
            
        logger.info(f"Loading pre-trained idiom matcher with SLOP={slop}...")
        # Determine which pattern file to load
        import json
        patterns_path = Path(__file__).parent / "patterns" / f"slop_{slop}.json"
            
        if not patterns_path.exists():
            raise FileNotFoundError(f"Pattern file not found: {patterns_path}. Make sure to run the build_patterns.py script first.")
            
        with open(patterns_path) as f:
            patterns = json.load(f)
        matcher = Idiomatcher(vocab)
        matcher.add_idiom_patterns(patterns)
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
            filtered_results = []
            
            # Add the longest match first
            filtered_results.append(results[0])
            
            # For each remaining match, check if it's contained in any accepted match
            for match in results[1:]:
                start, end = match['meta'][1], match['meta'][2]
                is_contained = any(
                    start >= f_match['meta'][1] and end <= f_match['meta'][2]
                    for f_match in filtered_results
                )
                
                if not is_contained:
                    filtered_results.append(match)
            
            return filtered_results
            
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

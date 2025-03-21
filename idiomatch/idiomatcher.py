from langcodes import Language
from spacy.matcher.matcher import Matcher
from spacy.tokens.doc import Doc
from spacy import Language
from tqdm import tqdm
import spacy
from loguru import logger
import yaml
from ._models._idiom import Idiom
from .builders import build
from .configs import NLP_MODEL, RESOURCES_DIR
from .builders import add_special_tok_cases


class Idiomatcher(Matcher):
    """Language
    a matcher class for.. matching idioms.
    """

    def __init__(self, nlp: Language, n: int, idioms: list[Idiom]):
        super().__init__(nlp.vocab)
        # we must maintain an nlp model here
        self.nlp = nlp
        self.n = n  # slop value
        self.idioms = idioms

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
        except OSError:
            logger.info(f"Model '{NLP_MODEL}' not found. Downloading it now...")
            try:
                spacy.cli.download(NLP_MODEL)
                logger.info(f"Successfully downloaded {NLP_MODEL}")
                nlp = spacy.load(NLP_MODEL)
            except Exception as e:
                raise OSError(
                    f"Failed to download spaCy model '{NLP_MODEL}'. Error: {str(e)}\n"
                    "Please try downloading it manually by running:\n"
                    f"python -m spacy download {NLP_MODEL}"
                )
        # then add special tokenization cases
        add_special_tok_cases(nlp)

        logger.info(f"Loading patterns with SLOP={n}...")
        # Determine which pattern file to load
        import json
        patterns_path = RESOURCES_DIR / f"slop_{n}.json"
            
        if not patterns_path.exists():
            raise FileNotFoundError(f"Pattern file not found: {patterns_path}. Make sure to run the build_patterns.py script first.")

        with open(RESOURCES_DIR / "idioms.yml") as f:
            idioms_data = yaml.safe_load(f)
        idioms = [Idiom(**idiom_data) for idiom_data in idioms_data]
        matcher = Idiomatcher(nlp, n, idioms)
        with open(patterns_path) as f:
            patterns = json.load(f)
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
        

    def add_idioms(self, idioms: list[dict]):
        """
        Build patterns for the given idiom and add them into the matcher.
        
        Args:
            idioms: List of idiom dictionaries to add
            
        Raises:
            ValueError: If any of the idioms already exist in the matcher
        """
        new_idioms = []
        duplicates = []
        for idiom_dict in idioms:
            idiom = Idiom(**idiom_dict)
            # Check if idiom already exists by comparing lemmas
            if any(existing.lemma == idiom.lemma for existing in self.idioms):
                duplicates.append(idiom.lemma)
                continue
            new_idioms.append(idiom)

        if duplicates:
            raise ValueError(f"The following idioms already exist in the matcher: {', '.join(duplicates)}")

        # add new idioms to the matcher
        self.idioms.extend(new_idioms)
        # build patterns and add them to the matcher
        patterns = build([idiom.lemma for idiom in new_idioms], self.nlp, self.n)
        for idiom, patterns in tqdm(patterns.items(),
                                    desc="adding patterns"):
            super().add(idiom, patterns)


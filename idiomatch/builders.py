from spacy import Language
from spacy.tokens import Token
from tqdm import tqdm
from idiomatch.configs import \
    TARGET_IDIOM_MIN_LENGTH, \
    TARGET_IDIOM_MIN_WORD_COUNT, \
    SLOP, WILDCARD

from idiomatch.cases import \
    IGNORED_CASES, \
    MORE_IDIOM_CASES, \
    PRP_PLACEHOLDER_CASES, \
    PRON_PLACEHOLDER_CASES, SPECIAL_TOK_CASES, OPTIONAL_CASES


# Utility functions for idiom processing

def norm_case(idiom: str) -> str:
    """Normalize the case of an idiom."""
    return idiom.lower() \
        .replace("i ", "I ") \
        .replace(" i ", " I ") \
        .replace("i'm", "I'm") \
        .replace("i'll", "I'll") \
        .replace("i\'d", "I'd")


def is_target(idiom: str) -> bool:
    """Determine if an idiom should be targeted for pattern building."""
    def above_min_word_count(idiom_: str) -> bool:
        return len(idiom_.split(" ")) >= TARGET_IDIOM_MIN_WORD_COUNT

    def above_min_length(idiom_: str) -> bool:
        return len(idiom_) >= TARGET_IDIOM_MIN_LENGTH

    def is_hyphenated(idiom_: str) -> bool:
        return "-" in idiom_

    return (idiom not in IGNORED_CASES) \
           and (above_min_word_count(idiom) or
                above_min_length(idiom) or
                is_hyphenated(idiom))


def prepare_idioms(slide_idioms: list[str]) -> list[str]:
    """Process raw idioms to create a filtered and normalized list."""
    # Add additional idiom cases
    all_idioms = slide_idioms + MORE_IDIOM_CASES
    
    # Filter and normalize
    return [norm_case(idiom) for idiom in all_idioms if is_target(idiom)]


def add_special_tok_cases(nlp: Language) -> None:
    """Add special token cases to the NLP pipeline."""
    for term, case in SPECIAL_TOK_CASES.items():
        nlp.tokenizer.add_special_case(term, case)


def insert_slop(patterns: list[dict], n: int) -> list[dict]:
    """
    Insert slop patterns between token patterns.
    (Implementation of intersperse: https://stackoverflow.com/a/5655780)
    """
    slop_pattern = [{"TEXT": {"REGEX": WILDCARD}, "OP": "?"}] * n  # insert n number of slops
    res = []
    is_first = True
    for pattern in patterns:
        if not is_first:
            res += slop_pattern
        res.append(pattern)
        is_first = False
    return res


def reorder(idiom_tokens: list[Token]) -> list[Token]:
    """
    Reorder tokens so that if the first token is a verb, it's moved to the end.
    e.g. call someone's bluff -> someone's bluff call
    """
    tokens = [token for token in idiom_tokens]
    if tokens[0].pos_ == "VERB":
        first = tokens.pop(0)
        tokens.append(first)  # put the token at the end
    return tokens


def build_modification(idiom_tokens: list[Token]) -> list[dict]:
    """Build pattern with slop."""
    pattern = [
        {"TAG": "PRP$"} if token.text in PRP_PLACEHOLDER_CASES  # one's, someone's
        else {"POS": "PRON"} if token.text in PRON_PLACEHOLDER_CASES  # someone.
        else {"TEXT": token.text, "OP": "?"} if token.text in OPTIONAL_CASES
        else {"LEMMA": {"REGEX": r"(?i)^{}$".format(token.lemma_)}}
        for token in idiom_tokens
    ]
    # insert slop over the pattern
    return insert_slop(pattern, SLOP)


def build_hyphenated(idiom_tokens: list[Token]) -> list[dict]:
    """Build pattern for hyphenated expressions with optional hyphen."""
    pattern = [
        {"TEXT": token.text, "OP": "?"} if token.text == "-"
        # Don't use lemma (this is to avoid false-positives)
        # Using regexp for case-insensitive match
        else {"TEXT": {"REGEX": r"(?i)^{}$".format(token.text)}}
        for token in idiom_tokens
    ]
    # Wrap the pattern in a list, since matcher.add() expects a list of patterns
    # Each pattern is itself a list of token dicts
    return [pattern]


def build_openslot(idiom_tokens: list[Token]) -> list[dict]:
    """Build pattern with wildcard and slop."""
    pattern = [
        # use a wildcard for placeholder cases.
        {"TEXT": {"REGEX": WILDCARD}} if token.text in (PRP_PLACEHOLDER_CASES + PRON_PLACEHOLDER_CASES)
        else {"TEXT": token.text, "OP": "?"} if token.text in OPTIONAL_CASES
        else {"LEMMA": {"REGEX": r"(?i)^{}$".format(token.lemma_)}}
        for token in idiom_tokens
    ]
    return insert_slop(pattern, SLOP)


def build_passivisation_with_modification(idiom_tokens: list[Token]) -> list[dict]:
    """Build pattern with reordering and slop."""
    tokens = reorder(idiom_tokens)
    return build_modification(tokens)


def build_passivisation_with_openslot(idiom_tokens: list[Token]) -> list[dict]:
    """Build pattern with reordering, wildcard, and slop."""
    tokens = reorder(idiom_tokens)
    return build_openslot(tokens)


def build_idiom_patterns(idioms: list[str], nlp: Language) -> dict[str, list]:
    """
    Build patterns for a list of idioms.
    
    Args:
        idioms: list of idioms to process
        nlp: Spacy Language model
        
    Returns:
        dictionary mapping idioms to their patterns
    """
    add_special_tok_cases(nlp)
    idiom_patterns = {}
    
    for idiom in tqdm(idioms, desc="Building patterns"):
        idiom_tokens = list(nlp(idiom))
        
        # Build all pattern types
        pattern_groups = [
            build_modification(idiom_tokens),
            build_openslot(idiom_tokens),
            build_passivisation_with_modification(idiom_tokens),
            build_passivisation_with_openslot(idiom_tokens)
        ]
        
        # Handle hyphenated separately as it may return a list of patterns
        hyphenated_patterns = build_hyphenated(idiom_tokens)
        if isinstance(hyphenated_patterns, list) and hyphenated_patterns and isinstance(hyphenated_patterns[0], list):
            # If it's a list of patterns, extend pattern_groups with each pattern
            pattern_groups.extend(hyphenated_patterns)
        else:
            # Otherwise add it as a single pattern group
            pattern_groups.append(hyphenated_patterns)
        
        # Filter out empty patterns
        patterns = [pattern for pattern in pattern_groups if pattern]
        
        # Add to results dictionary
        idiom_patterns[idiom] = patterns
        
    return idiom_patterns

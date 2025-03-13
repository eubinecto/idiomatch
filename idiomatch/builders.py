from spacy import Language
from spacy.tokens import Token
from tqdm import tqdm
from idiomatch.configs import WILDCARD

from idiomatch.cases import \
    PRP_PLACEHOLDER_CASES, \
    PRON_PLACEHOLDER_CASES, SPECIAL_TOK_CASES, OPTIONAL_CASES



# # Utility functions for idiom processing

# def norm_case(idiom: str) -> str:
#     """Normalize the case of an idiom."""
#     return idiom.lower() \
#         .replace("i ", "I ") \
#         .replace(" i ", " I ") \
#         .replace("i'm", "I'm") \
#         .replace("i'll", "I'll") \
#         .replace("i\'d", "I'd")


# def is_target(idiom: str) -> bool:
#     """Determine if an idiom should be targeted for pattern building."""
#     def above_min_word_count(idiom_: str) -> bool:
#         return len(idiom_.split(" ")) >= TARGET_IDIOM_MIN_WORD_COUNT

#     def above_min_length(idiom_: str) -> bool:
#         return len(idiom_) >= TARGET_IDIOM_MIN_LENGTH

#     def is_hyphenated(idiom_: str) -> bool:
#         return "-" in idiom_

#     return (idiom not in IGNORED_CASES) \
#            and (above_min_word_count(idiom) or
#                 above_min_length(idiom) or
#                 is_hyphenated(idiom))


# def prepare_idioms(slide_idioms: list[str]) -> list[str]:
#     """Process raw idioms to create a filtered and normalized list."""
#     # Add additional idiom cases
#     all_idioms = slide_idioms + MORE_IDIOM_CASES
    
#     # Filter and normalize
#     return [norm_case(idiom) for idiom in all_idioms if is_target(idiom)]


def add_special_tok_cases(nlp: Language) -> None:
    """Add special token cases to the NLP pipeline."""
    for term, case in SPECIAL_TOK_CASES.items():
        nlp.tokenizer.add_special_case(term, case)


def slop(patterns: list[dict], n: int) -> list[dict]:
    """
    Insert slop patterns between token patterns.
    The slop value n determines the maximum number of words that can appear
    between tokens in the idiom. For example:
    - With slop=1: "I can [1 word] tell you" is matched, but "I can [2 words] tell you" is not.
    - With slop=3: "I can [up to 3 words] tell you" is matched, but "I can [4+ words] tell you" is not.
    - With slop=5: "I can [up to 5 words] tell you" is matched, but "I can [6+ words] tell you" is not.
    """
    new = []
    # For each token pair, add appropriate slop between them
    for i in range(len(patterns)):
        new.append(patterns[i])
        if i < len(patterns) - 1:
            # For higher slop values, we need 0 to n words
            new.append({"TEXT": {"REGEX": WILDCARD}, "OP": "{0," + str(n) + "}"})        
    return new


def openslot(tokens: list[Token], n) -> list[dict]:
    """Build pattern with modifications."""
    pattern = [
        {"TAG": "PRP$"} if token.text in PRP_PLACEHOLDER_CASES  # one's, someone's
        else {"POS": "PRON"} if token.text in PRON_PLACEHOLDER_CASES  # someone.
        else {"TEXT": token.text, "OP": "?"} if token.text in OPTIONAL_CASES  # e.g. commas
        else {"LEMMA": {"REGEX": fr"(?i)^{token.lemma_}$"}}
        for token in tokens
    ]
    return slop(pattern, n)


def hyphenated(tokens: list[Token], n) -> list[dict]:
    """Build pattern for hyphenated expressions with optional hyphen."""
    pattern = [
        {"TEXT": token.text, "OP": "?"} if token.text == "-"
        # Don't use lemma (this is to avoid false-positives)
        # Using regexp for case-insensitive match
        else {"TEXT": {"REGEX": fr"(?i)^{token.text}$"}}
        for token in tokens
    ]
    assert isinstance(pattern, list)
    return slop(pattern, n)


def reorder(tokens: list[Token]) -> list[Token]:
    """
    Reorder tokens so that if the first token is a verb, it's moved to the end.
    e.g. call someone's bluff -> someone's bluff call
    """
    tokens = [token for token in tokens]
    if tokens[0].pos_ == "VERB":
        first = tokens.pop(0)
        tokens.append(first)  # put the token at the end
    return tokens


def openslot_passive(tokens: list[Token], n: int) -> list[dict]:
    """Build pattern with reordering and wildcard."""
    tokens = reorder(tokens)
    patterns = openslot(tokens, n)
    return slop(patterns, n)


def default(tokens: list[Token], n: int) -> list[dict]:
    """Build default pattern."""
    patterns = [
        # use lemma for default cases. Use Regex for case-insensitive match
        {"LEMMA": {"REGEX": fr"(?i)^{token.lemma_}$"}}
        for token in tokens
    ]
    return slop(patterns, n)


def build(idioms: list[str], nlp: Language, n: int) -> dict[str, list]:
    """
    Build patterns for a list of idioms.
    
    Args:
        idioms: list of idioms to process
        nlp: Spacy Language model
        slop: maximum number of words allowed between pattern tokens (default: 3)
    Returns:
        dictionary mapping idioms to their patterns
    """
    add_special_tok_cases(nlp)
    idiom2patterns: dict[str, list[list[dict]]] = {}  # this is the one to build for
    for idiom in tqdm(idioms):
        patterns = []
        doc = nlp(idiom)
        # if it's hyphenated, build a pattern for it
        if "-" in idiom:
            patterns.append(hyphenated(doc, n))
        # if it includes openslot, build a pattern for it
        elif set(PRON_PLACEHOLDER_CASES + PRP_PLACEHOLDER_CASES + OPTIONAL_CASES).intersection(set(tok.text for tok in doc)) \
            and idiom not in ["something like", "something awful"]:  # cases where something is not an openslot
            patterns.append(openslot(doc, n))
            patterns.append(openslot_passive(doc, n))
        # else, just add default patterns
        else:
            patterns.append(default(doc, n))
        idiom2patterns[idiom] = patterns
    return idiom2patterns

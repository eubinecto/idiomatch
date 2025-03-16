# spacy - the base model to use.
from pathlib import Path

NLP_MODEL = "en_core_web_sm"

# target idiom settings
TARGET_IDIOM_MIN_LENGTH = 14
TARGET_IDIOM_MIN_WORD_COUNT = 3

WILDCARD = r"[a-zA-Z0-9,\-\'\"]+"

# for patterns and idioms
RESOURCES_DIR = Path(__file__).parent / "resources"

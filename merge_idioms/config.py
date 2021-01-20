from pathlib import Path
from os import path

# the root directory of this project
# define the directories here
PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent
LIB_ROOT_DIR = Path(__file__).resolve().parent

# external data
DATA_DIR = path.join(PROJECT_ROOT_DIR, "data")
SLIDE_DIR = path.join(DATA_DIR, "slide")
SLIDE_TSV = path.join(SLIDE_DIR, "slide.tsv")
# html's are utf-8 encoded
SLIDE_IDIOM_ALTS_TSV = path.join(SLIDE_DIR, 'slide_idiom_alts.tsv')

# resources needed for the library
RESRCS_DIR = path.join(LIB_ROOT_DIR, "resources")
TARGET_IDIOMS_TXT = path.join(RESRCS_DIR, "target_idioms.txt")
# reduce them to just these two files. They are what goes into resources directory.
IDIOM_PATTERNS_TSV = path.join(RESRCS_DIR, "idiom_patterns.tsv")
IDIOM_ALTS_TSV = path.join(RESRCS_DIR, "idiom_alts.tsv")

# metadata for merge-idiom-pipeline
MIP_NAME = 'mip'
MIP_VERSION = "0.0.10"

# spacy - the base model to use.
BASE_NLP_MODEL = "en_core_web_sm"

# target idiom settings
TARGET_IDIOM_MIN_LENGTH = 14
TARGET_IDIOM_MIN_WORD_COUNT = 3

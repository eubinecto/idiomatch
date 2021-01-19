from pathlib import Path
from os import path

# the root directory of this project
# define the directories here
PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent
LIB_ROOT_DIR = Path(__file__).resolve().parent

# external data
DATA_DIR = path.join(PROJECT_ROOT_DIR, "data")
SLIDE_DIR = path.join(DATA_DIR, "slide")
SLIDE_TSV_PATH = path.join(SLIDE_DIR, "slide.tsv")

# resources needed for the library
RESRCS_DIR = path.join(LIB_ROOT_DIR, "resources")
IDIOM_PATTERNS_JSON_PATH = path.join(RESRCS_DIR, "idiom_patterns.json")
IDIOM_PATTERNS_CSV_PATH = path.join(RESRCS_DIR, "idiom_patterns.csv")  # just so that people can view it on github
TARGET_IDIOMS_TXT_PATH = path.join(RESRCS_DIR, "target_idioms.txt")
TARGET_IDIOMS_JSON_PATH = path.join(RESRCS_DIR, "target_idioms.json")
TARGET_IDIOMS_CSV_PATH = path.join(RESRCS_DIR, "target_idioms.csv")  # just so that people can view it on github

# metadata for merge-idiom-pipeline
MIP_NAME = 'mip'
MIP_VERSION = "0.0.10"
MIP_MODEL_PATH = path.join(DATA_DIR, MIP_NAME + "_" + MIP_VERSION)

# spacy - the base model to use.
NLP_MODEL_NAME = "en_core_web_sm"

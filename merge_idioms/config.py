from pathlib import Path
from os import path
from datetime import datetime


# to log everything. I'll put date and time to everything.
def now() -> str:
    now_obj = datetime.now()
    return now_obj.strftime("%d_%m_%Y__%H_%M_%S")


# to be used by other models
now_str = now()

# the root directory of this project
# define the directories here
PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent
LIB_ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = path.join(PROJECT_ROOT_DIR, "data")  # maybe if you want to save it.
CACHES_DIR = path.join(LIB_ROOT_DIR, "caches")
SLIDE_DIR = path.join(LIB_ROOT_DIR, "slide")


# caches to be version controlled (and to be used by library)
IDIOM_PATTERNS_JSON_PATH = path.join(CACHES_DIR, "idiom_patterns.json")
IDIOM_PATTERNS_CSV_PATH = path.join(CACHES_DIR, "idiom_patterns.csv")

# slide tsv data.
SLIDE_TSV_PATH = path.join(SLIDE_DIR, "slide.tsv")

# the model to use outside of this repo
MIP_MODEL_PATH = path.join(DATA_DIR, 'mip_model')

# spacy - the model to use.
NLP_MODEL = "en_core_web_sm"

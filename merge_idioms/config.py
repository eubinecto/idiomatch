from pathlib import Path
from os import path
from datetime import datetime


# to log everything. I'll put date and time to everything.
def now() -> str:
    now_obj = datetime.now()
    return now_obj.strftime("%d_%m_%Y__%H_%M_%S")


# to be used for saving different versions of data
now_str = now()

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
IDIOM_PATTERNS_CSV_PATH = path.join(RESRCS_DIR, "idiom_patterns.csv")  # just so that people can view it
TARGET_IDIOMS_TXT_PATH = path.join(RESRCS_DIR, "target_idioms.txt")


# the model to use outside of this repo
MIP_NAME = 'mip'
MIP_VERSION = "0.0.1"
MIP_MODEL_PATH = path.join(DATA_DIR, MIP_NAME + "_" + MIP_VERSION)

# spacy - the base model to use.
NLP_MODEL_NAME = "en_core_web_sm"

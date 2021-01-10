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
# local data are stored here.
DATA_DIR = path.join(PROJECT_ROOT_DIR, "data")
# to be distributed
RESRCS_DIR = path.join(PROJECT_ROOT_DIR, "resources")

# the directories to store resources in
IDIOMS_DIR = path.join(RESRCS_DIR, "idioms")
SLIDE_DIR = path.join(RESRCS_DIR, "slide")

# resources for idioms
IDIOM_PATTERNS_JSON_PATH = path.join(IDIOMS_DIR, "idiom_patterns.json")
IDIOM_PATTERNS_CSV_PATH = path.join(IDIOMS_DIR, "idiom_patterns.csv")
TARGET_IDIOMS_TXT_PATH = path.join(IDIOMS_DIR, "target_idioms.txt")

# resources for slide
SLIDE_TSV_PATH = path.join(SLIDE_DIR, "slide.tsv")

# the model to use outside of this repo
MIP_MODEL_PATH = path.join(DATA_DIR, 'mip_model')

# spacy - the model to use.
NLP_MODEL = "en_core_web_sm"

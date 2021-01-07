from pathlib import Path
from os import path
from datetime import datetime
# the root directory of this project
# define the directories here
ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = path.join(ROOT_DIR, "data")


# to log everything. I'll put date and time to everything.
def now() -> str:
    now_obj = datetime.now()
    return now_obj.strftime("%d_%m_%Y__%H_%M_%S")


# to be used by other models
now_str = now()

# data directories
SLIDE_DIR = path.join(DATA_DIR, "slide")
MATCHER_DIR = path.join(DATA_DIR, "matcher")
PIPELINE_DIR = path.join(DATA_DIR, "pipeline")


# slide data
SLIDE_TSV_PATH = path.join(SLIDE_DIR, "slide.tsv")


# matcher data
IDIOM_MATCHER_PKL_CURR_PATH = path.join(MATCHER_DIR, "idiom_matcher_07_01_2021__14_33_00.pkl")
IDIOM_MATCHER_PKL_PATH = path.join(MATCHER_DIR, 'idiom_matcher_{}.pkl'.format(now_str))
IDIOM_MATCHER_INFO_TSV_PATH = path.join(MATCHER_DIR, "idiom_matcher_info_{}.tsv".format(now_str))

# pipeline data
MIP_PATH = path.join(PIPELINE_DIR, "mip_{}".format(now_str))

# spacy
NLP_MODEL = "en_core_web_sm"

# for tsv files
DELIM = "\t"

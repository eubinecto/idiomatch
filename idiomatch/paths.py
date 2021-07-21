from pathlib import Path
from os import path

# the root directory of this project
# define the directories here
PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent.__str__()
LIB_ROOT_DIR = path.join(PROJECT_ROOT_DIR, "idiomatch")
# external data
DATA_DIR = path.join(PROJECT_ROOT_DIR, "data")
SLIDE_DIR = path.join(DATA_DIR, "slide")
SLIDE_TSV = path.join(SLIDE_DIR, "slide.tsv")

# resources needed for the library
RESRCS_DIR = path.join(LIB_ROOT_DIR, "resources")
TARGET_IDIOMS_TXT = path.join(RESRCS_DIR, "target_idioms.txt")
# reduce them to just these two files. They are what goes into resources directory.
IDIOM_PATTERNS_TSV = path.join(RESRCS_DIR, "idiom_patterns.tsv")
IDIOMS_TXT = path.join(RESRCS_DIR, "idioms.txt")

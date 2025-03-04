import json
import spacy
from idiomatch.builders import IdiomPatternsBuilder
from loguru import logger
from pathlib import Path

def main():
    # save the idiom_patterns
    with open(Path(__file__).parent / "idioms.txt") as f:
        idioms = [line.strip() for line in f if line.strip()]
    # load an nlp object
    nlp = spacy.load("en_core_web_sm")
    patterns = IdiomPatternsBuilder(nlp).construct(idioms)
    # Save directly as a JSON file
    with open(Path(__file__).parent.parent / "idiomatch" / "patterns.json", 'w') as f:
        json.dump(patterns, f, indent=2)
    logger.info(f"Successfully saved idiom patterns to {Path(__file__).parent.parent / 'idiomatch' / 'patterns.json'}")


if __name__ == '__main__':
    main()

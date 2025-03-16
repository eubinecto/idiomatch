import json
from langcodes import Language
import spacy
import yaml
import glob
import pandas as pd
from pathlib import Path
from idiomatch.builders import build, add_special_tok_cases
from idiomatch.configs import RESOURCES_DIR, NLP_MODEL
from idiomatch import Idiom, Sense
from loguru import logger
import concurrent.futures
import click
from tqdm import tqdm


def upidioms():
    """Update idioms.yml file with new idioms."""
    # Load the source information from idiomLexicon.tsv
    lexicon_path = Path("scripts/corpus/slide/idiomLexicon.tsv")
    lexicon_df = pd.read_csv(lexicon_path, sep='\t')
    # Create a dictionary mapping idioms to their Wiktionary URLs
    source_map = dict(zip(lexicon_df['Idiom'], lexicon_df['WiktionaryURL']))
    
    # Get all batch files
    batch_files = glob.glob("scripts/corpus/slide/parsed/batch-*.yaml")
    idioms = []
    
    # Process each batch file
    for batch_file in tqdm(batch_files, desc="Processing batch files"):
        with open(batch_file, 'r') as f:
            batch_data = yaml.safe_load(f)
            if not batch_data:  # Skip empty files
                continue
            # Process each idiom entry in the batch
            for entry in batch_data:
                phrase = entry['phrase']
                response = entry['response']
                if response is None:
                    logger.warning(f"No response found for idiom: {phrase}")
                    continue
                etymology = response["etymology"]
                # Create Sense objects for each sense
                senses = []
                if response and 'senses' in response:
                    for sense_data in response['senses']:
                        sense = Sense(
                            content=sense_data['content'].strip(),
                            examples=sense_data.get("examples", [])
                        )
                        senses.append(sense)
                
                # Create Idiom object
                source = source_map[phrase]  # Get source URL from lexicon
                idiom = Idiom(
                    lemma=phrase,
                    etymology=etymology,
                    senses=senses,
                    source=source
                )
                idioms.append(idiom)
    # add missing idioms manually
    idioms.append(
        Idiom(
            lemma="Catch-22",
            etymology="Coined by American author Joseph Heller in 1961 in his novel Catch-22, in which the main character feigns madness in order to avoid dangerous combat missions, but his desire to avoid them is taken to prove his sanity.",
            senses=[
                Sense(
                    content="(idiomatic) A difficult situation from which there is no escape because it involves mutually conflicting or dependent conditions.",
                    examples=["For us it’s been a real Catch-22: when we have the time to take a vacation, we don’t have enough money, and when we have enough money, we don’t have the time."]
                )
            ],
            source="https://en.wiktionary.org/wiki/Catch-22"
        )
    )
    idioms.append(
        Idiom(
            lemma="come down to earth",
            etymology=None,
            senses=[
                Sense(
                    content="(idiomatic, of an event, thing, person) To be brought back to reality; to emerge from a daydream.",
                    examples=["So many good things have been happening for me, and I've just been such a happy man. I've wanted to write earlier but couldn't come down to earth long enough."]
                )
            ],
            source="https://en.wiktionary.org/wiki/come_down_to_earth"
        )
    )
    idioms.append(
        Idiom(
            lemma="beat around the bush",
            etymology="From the older form beat about the bush, replacing the preposition.",
            senses=[
                Sense(
                    content="(idiomatic) To treat a topic, but omit its main points, often intentionally.",
                    examples=[]
                ),
                Sense(
                    content="To delay or avoid talking about something difficult or unpleasant. ",
                    examples=["Just stop beating around the bush and tell me what the problem is!",
                             "Look here - said Smith, menacingly, if you think I cheated you, you might as well say so right out. I don't like beating around the bush."]
                )
            ],
            source="https://en.wiktionary.org/wiki/beat_around_the_bush"
        )
    )
    # Save the idioms to YAML file
    out_path = RESOURCES_DIR / "idioms.yml"
    with open(out_path, 'w') as f:
        yaml.dump([idiom.model_dump() for idiom in idioms], f, allow_unicode=True)
    
    logger.info(f"Successfully saved {len(idioms)} idioms to {out_path}")


def uppatterns():
    """Update all pattern files with different SLOP values."""
    def build_and_save(n: int, lemmas: list[str], nlp: Language):
        """Build patterns with the specified slop value and save them to a file."""
        logger.info(f"Building patterns with SLOP={n}")
        patterns = build(lemmas, nlp, n)
        # Save to a JSON file with the slop value in the filename
        out_path = RESOURCES_DIR / f"slop_{n}.json"
        with open(out_path, 'w') as f:
            json.dump(patterns, f, indent=2)
        logger.info(f"Successfully saved idiom patterns with SLOP={n} to {out_path}")
        return n
    # Load idioms
    with open(RESOURCES_DIR / "idioms.yml") as f:
        idioms_data = yaml.safe_load(f)
    idioms = [Idiom(**d) for d in idioms_data]
    lemmas = [idiom.lemma for idiom in idioms]
    # Load NLP model
    nlp = spacy.load(NLP_MODEL)
    # Build patterns with different SLOP values (1-5) in parallel
    logger.info("Starting parallel build of patterns with different SLOP values")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all tasks
        future_to_slop = {
            executor.submit(build_and_save, n, lemmas, nlp): n
            for n in range(1, 6)
        }
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_slop):
            n = future_to_slop[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error building patterns with SLOP={n}: {e}")


@click.command()
@click.argument('target', type=click.Choice(['idioms', 'patterns'], case_sensitive=False))
def main(target):
    """Update either idioms or patterns based on the target argument."""
    if target == 'patterns':
        uppatterns()
    else:  # target == 'idioms'
        upidioms()


if __name__ == '__main__':
    main()

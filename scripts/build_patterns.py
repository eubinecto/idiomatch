import json
import spacy
from idiomatch.builders import build_idiom_patterns
from loguru import logger
from pathlib import Path
import concurrent.futures

def build_patterns_with_slop(idioms, nlp, slop_value):
    """Build patterns with a specific slop value."""
    # Build patterns with the modified SLOP value
    patterns = build_idiom_patterns(idioms, nlp, slop_value)
    
    return patterns

def build_and_save_patterns(slop, idioms, nlp, patterns_dir):
    """Build patterns with the specified slop value and save them to a file."""
    logger.info(f"Building patterns with SLOP={slop}")
    patterns = build_patterns_with_slop(idioms, nlp, slop)
    
    # Save to a JSON file with the slop value in the filename
    output_file = patterns_dir / f"slop_{slop}.json"
    with open(output_file, 'w') as f:
        json.dump(patterns, f, indent=2)
    
    logger.info(f"Successfully saved idiom patterns with SLOP={slop} to {output_file}")
    return slop

def main():
    # Create patterns directory if it doesn't exist
    patterns_dir = Path(__file__).parent.parent / "idiomatch" / "patterns"
    patterns_dir.mkdir(exist_ok=True)
    
    # Load idioms
    with open(Path(__file__).parent / "idioms.txt") as f:
        idioms = [line.strip() for line in f if line.strip()]
    
    # Load NLP model
    nlp = spacy.load("en_core_web_sm")
    
    # Build patterns with different SLOP values (1-5) in parallel
    logger.info("Starting parallel build of patterns with different SLOP values")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all tasks
        future_to_slop = {
            executor.submit(build_and_save_patterns, slop, idioms, nlp, patterns_dir): slop
            for slop in range(1, 6)
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_slop):
            slop = future_to_slop[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error building patterns with SLOP={slop}: {e}")
    


if __name__ == '__main__':
    main()

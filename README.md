# identify-idioms

Implementation of custom Pipeline Component in [SpaCy(3.0)](https://nightly.spacy.io) for identifying idioms as atomic tokens.

## Install

install the library:
```
pip3 install identify-idioms
```
download Spacy's core model for English:
```
python3 spacy -m download en_core_web_sm
```

## Quick Start
```python
import spacy
from identify_idioms import IdiomMatcher


def main():

    sentences = [
        "You are down to earth.",
        "Have you found your feet on the new job?",
    ]

    nlp = spacy.load("en_core_web_sm")  # idiom matcher needs an nlp pipeline. Currently supports en_core_web_sm only.
    idiom_matcher = IdiomMatcher.from_pretrained(nlp)  # this will take approx 40 seconds.

    for sent in sentences:
        # process the sentence
        doc = nlp(sent)
        # identify all
        matches = idiom_matcher(doc)
        for token_id, start, end in matches:
            print(nlp.vocab.strings[token_id], start, end)
        print("-----")


if __name__ == '__main__':
    main()

```

## Supported Idioms
List of supported idioms with matching patterns can be found in [`identify-idioms/identify_idioms/resources/idiom_patterns.csv`](https://github.com/eubinecto/identify-idioms/blob/main/identify_idioms/resources/idiom_patterns.tsv). Total of 2758 idioms are available for
matching & merging. These "target idioms" were extracted from a vocabulary of 5000 most 
frequently used English idioms, which had been made available for open use courtesy of [IBM's SLIDE project](https://developer.ibm.com/exchanges/data/all/sentiment-lexicon-of-idiomatic-expressions/). 

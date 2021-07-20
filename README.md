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

# examples sentences
sentences = [
        "You are down to earth.",
        "Have you found your feet on the new job?",
        "To ask our members to accept a pay cut heaps insult on injury."
    ]


# build a spacy pipeline for identifying idioms, based off of en_core_web_sm model
nlp = spacy.load("en_core_web_sm")
idiom_matcher = IdiomMatcher.from_pretrained(nlp.vocab)


for sent in sentences:
    # process the sentence
    doc = iip(sent)
    # idioms are identified as atomic tokens in tokenisation process
    token_texts = [token.text for token in doc]
    # supports lemmatization of idioms as well
    token_lemmas = [token.lemma_ for token in doc]
    # is_idiom custom attribute can be used to filter idioms
    token_idioms = [token.lemma_ for token in doc if token._.is_idiom]

    print("tokenisation:", token_texts)
    print("lemmatisation:", token_lemmas)
    print("filtering:", token_idioms)
    print("-----------")

```
output:
```
tokenisation: ['You', 'are', 'down to earth', '.']
lemmatisation: ['you', 'be', 'down-to-earth', '.']
filtering: ['down-to-earth']
-----------
tokenisation: ['Have', 'you', 'found your feet', 'on', 'the', 'new', 'job', '?']
lemmatisation: ['have', 'you', "find one's feet", 'on', 'the', 'new', 'job', '?']
filtering: ["find one's feet"]
-----------
tokenisation: ['To', 'ask', 'our', 'members', 'to', 'accept', 'a', 'pay', 'cut', 'heaps insult on injury', '.']
lemmatisation: ['to', 'ask', 'our', 'member', 'to', 'accept', 'a', 'pay', 'cut', 'add insult to injury', '.']
filtering: ['add insult to injury']
-----------
```

## Supported Idioms
List of supported idioms with matching patterns can be found in [`identify-idioms/identify_idioms/resources/idiom_patterns.csv`](https://github.com/eubinecto/identify-idioms/blob/main/identify_idioms/resources/idiom_patterns.tsv). Total of 2758 idioms are available for
matching & merging. These "target idioms" were extracted from a vocabulary of 5000 most 
frequently used English idioms, which had been made available for open use courtesy of [IBM's SLIDE project](https://developer.ibm.com/exchanges/data/all/sentiment-lexicon-of-idiomatic-expressions/). 

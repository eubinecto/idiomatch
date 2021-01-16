# merge-idioms
Implementation of custom component in [SpaCy(3.0)](https://nightly.spacy.io) for merging idioms into stand-alone tokens.

## install

install the library:
```
pip3 install merge-idioms
```
download Spacy's English core model:
```
python3 spacy -m download en_core_web_sm
```

## Quick Start
```python
from merge_idioms import build_mip

sentences = [
    "At the end of the day, your fate is on your hands.",
    "She claimed that it was a Catch 22 situation for her.",
    "they were teaching me a lesson for daring to complain."
]
# build a spacy pipeline for merging idioms, based off of en_core_web_sm model
mip = build_mip()

for sent in sentences:
    # process the sentence
    doc = mip(sent)
    # idioms are merged to standalone tokens
    token_texts = [token.text for token in doc]
    # supports lemmatization as well
    token_lemmas = [token.lemma_ for token in doc]
    # is_idiom custom attribute could be used to identify idioms
    token_idioms = [token.lemma_ for token in doc if token._.is_idiom]

    print("tokenisation:",token_texts)
    print("lemmatisation:", token_lemmas)
    print("filtering:", token_idioms)
    print("-----------")

```
output:
```
tokenisation: ['At the end of the day', ',', 'your', 'fate', 'is', 'on your hands', '.']
lemmatisation: ['at the end of the day', ',', 'your', 'fate', 'be', "on one's hands", '.']
filtering: ['at the end of the day', "on one's hands"]
-----------
tokenisation: ['She', 'claimed', 'that', 'it', 'was', 'a', 'Catch 22', 'situation', 'for', 'her', '.']
lemmatisation: ['she', 'claim', 'that', 'it', 'be', 'a', 'catch-22', 'situation', 'for', 'she', '.']
filtering: ['catch-22']
-----------
tokenisation: ['they', 'were', 'teaching me a lesson', 'for', 'daring', 'to', 'complain', '.']
lemmatisation: ['they', 'be', 'teach someone a lesson', 'for', 'dare', 'to', 'complain', '.']
filtering: ['teach someone a lesson']
-----------
```
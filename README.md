# merge-idioms
Implementation of Spacy's NLP pipeline for merging idioms as standalone tokens. 


## Quick Start
```python

from merge_idioms import MIPBuilder
mip_builder = MIPBuilder()
mip_builder.construct()
# merge-idiom-pipeline
mip = mip_builder.mip

# example sentence that includes an idiom
sent = " but there comes a time when one has to draw a line in the sand."
# execute pipeline
doc = mip(sent)
# get the lemmas & tags
lemmas = [token.lemma_ for token in doc]
print(lemmas)
```
```
['at the end of the day', ',', 'your', 'fate', 'be', "on one's hands", '.']
```
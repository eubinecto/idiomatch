# idiomatch

An implementation of [SpaCy(3.0)](https://nightly.spacy.io)'s `Matcher` specifically designed for identifying English idioms.


## Quick Start


Install the library via uv (or whatever package manager you prefer)
```bash
uv add idiomatch 
```

```python3
import spacy
from idiomatch import Idiomatcher

def main():
    sent = "The floodgates will remain opened for a host of new lawsuits."  # a usecase of *open the floodgates*
    nlp = spacy.load("en_core_web_sm")  # idiom matcher needs an nlp pipeline; Currently supports en_core_web_sm only.
    idiomatcher = Idiomatcher.from_pretrained(nlp.vocab)  # this will take approx 50 seconds.
    doc = nlp(sent)  # process the sentence with an nlp pipeline
    print(idiomatcher(doc))  # identify the idiom in the sentence


if __name__ == '__main__':
    main()

```
```
adding patterns into idiom_matcher...: 100%|██████████| 2756/2756 [00:52<00:00, 52.83it/s]
[{'idiom': 'open the floodgates', 'span': 'The floodgates will remain opened', 'meta': (13612509636477658373, 0, 5)}]
```

## Supported Idioms
List of supported idioms can be found in `idiomatch/resources/idioms.txt`. Total of 2758 idioms are available for
matching. These "target idioms" were extracted from a vocabulary of 5000 most 
frequently used English idioms, which had been made available for open use courtesy of [IBM's SLIDE project](https://developer.ibm.com/exchanges/data/all/sentiment-lexicon-of-idiomatic-expressions/).


## Adding Idioms Yourself

If you have idioms that are not included in the list of supported idioms, you can add them to `Idiomatcher`
yourself with the `add_idioms` member method:

```python3
import spacy
from idiomatch import Idiomatcher


def main():
    nlp = spacy.load("en_core_web_sm")
    idiomatcher = Idiomatcher.from_pretrained(nlp.vocab)  # instantiate 
    # As for a placeholder for openslot, use either: someone / something / someone's / one's 
    idioms = ["have blood on one's hands"]
    idiomatcher.add_idioms(nlp, idioms)  # this will train idiomatcher to identify the given idioms
    sent = "The leaders of this war have the blood of many thousands of people on their hands."
    doc = nlp(sent)
    print(idiomatcher(doc))


if __name__ == '__main__':
    main()
```
```
100%|██████████| 2/2 [00:00<00:00, 145.62it/s]
adding patterns into idiom_matcher...: 100%|██████████| 2/2 [00:00<00:00, 196.40it/s]
[{'idiom': "have blood on one's hands", 'span': 'have the blood of many thousands of people on their hands', 'meta': (5930902300252675198, 5, 16)}]
```

## Supported Variations

English idioms extensively vary in forms, at least in six different ways. `Idiomatcher` can gracefully handle all the 
cases, as exemplified below:


variation | example | result
--- | --- | --- 
modification | *He **called my blatant bluff*** | `[{'idiom': "call someone's bluff", 'span': 'called my blatant bluff', 'meta': (11321959191976266509, 1, 5)}]`
openslot | *This will **keep all of us posted*** | `[{'idiom': 'keep someone posted', 'span': 'keep all of us posted', 'meta': (11722464987668971331, 2, 7)}]`
hyphenated | *That was one **balls-out** street race!* | `[{'idiom': 'balls-out', 'span': 'balls - out', 'meta': (2876800142358111704, 3, 6)}]`
hyphen omitted | *That was one **balls out** street race!* | `[{'idiom': 'balls-out', 'span': 'balls out', 'meta': (2876800142358111704, 3, 5)}]`
passivisation (modification) | ***the floodgates are finally opened*** | `[{'idiom': 'open the floodgates', 'span': 'the floodgates are finally opened', 'meta': (13612509636477658373, 0, 5)}]`
passivisation (openslot) | ***my bluff was embarrassingly called** by her* | `[{'idiom': "call someone's bluff", 'span': 'my bluff was embarrassingly called', 'meta': (11321959191976266509, 0, 5)}]`
inclusion | *If she dies, you wil **have her blood on your hands**!* | `[{'idiom': "have blood on one's hands", 'span': 'have her blood on your hands', 'meta': (5930902300252675198, 6, 12)}, {'idiom': "on one's hands", 'span': 'on your hands', 'meta': (8246625119345375174, 9, 12)}]`



## How Does it Work?

The idiom-matching patterns, which are the foundations of `Idiomatcher`'s flexibility, are heavily inspired by Hughs et al.'s briliant work (2021) on [*Flexible Retrieval of Idiomatic Expressions from a Large Text Corpus*](https://www.mdpi.com/1019008).

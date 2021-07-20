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
        "He called my blatant bluff",  # modification
        "This will keep all of us posted",  # openslot
        "That was one balls-out street race!",  # hyphenated
        "That was one balls out street race!",  # hyphen omitted
        "the floodgates are finally opened",  # passivisation with modification
        "my bluff was embarrassingly called by her",   # passivisation with openslot
        "If she dies, you wil have her blood on your hands!"  # inclusion
    ]

    nlp = spacy.load("en_core_web_sm")  # idiom matcher needs an nlp pipeline. Currently supports en_core_web_sm only.
    idiom_matcher = IdiomMatcher.from_pretrained(nlp)  # this will take approx 40 seconds.

    sent = sentences[0]
    print("modification: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))  # use the method identify.
    sent = sentences[1]
    print("openslot: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))
    sent = sentences[2]
    print("hyphenated: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))
    sent = sentences[3]
    print("hyphen omitted: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))
    sent = sentences[4]
    print("passivisation (modification): {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))
    sent = sentences[5]
    print("passivisation (openslot): {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))
    sent = sentences[6]
    print("inclusion: {} -> {}".format(sent, idiom_matcher.identify(nlp(sent))))


if __name__ == '__main__':
    main()
```
```
modification: He called my blatant bluff -> [{'idiom': "call someone's bluff", 'span': 'called my blatant bluff', 'meta': (11321959191976266509, 1, 5)}]
openslot: This will keep all of us posted -> [{'idiom': 'keep someone posted', 'span': 'keep all of us posted', 'meta': (11722464987668971331, 2, 7)}]
hyphenated: That was one balls-out street race! -> [{'idiom': 'balls-out', 'span': 'balls - out', 'meta': (2876800142358111704, 3, 6)}]
hyphen omitted: That was one balls out street race! -> [{'idiom': 'balls-out', 'span': 'balls out', 'meta': (2876800142358111704, 3, 5)}]
passivisation (modification): the floodgates are finally opened -> [{'idiom': 'open the floodgates', 'span': 'the floodgates are finally opened', 'meta': (13612509636477658373, 0, 5)}]
passivisation (openslot): my bluff was embarrassingly called by her -> [{'idiom': "call someone's bluff", 'span': 'my bluff was embarrassingly called', 'meta': (11321959191976266509, 0, 5)}]
inclusion: If she dies, you wil have her blood on your hands! -> [{'idiom': "have blood on one's hands", 'span': 'have her blood on your hands', 'meta': (5930902300252675198, 6, 12)}, {'idiom': "on one's hands", 'span': 'on your hands', 'meta': (8246625119345375174, 9, 12)}]
```

## From pretrained?
List of supported idioms with matching patterns can be found in [`identify-idioms/identify_idioms/resources/idiom_patterns.csv`](https://github.com/eubinecto/identify-idioms/blob/main/identify_idioms/resources/idiom_patterns.tsv). Total of 2758 idioms are available for
matching & merging. These "target idioms" were extracted from a vocabulary of 5000 most 
frequently used English idioms, which had been made available for open use courtesy of [IBM's SLIDE project](https://developer.ibm.com/exchanges/data/all/sentiment-lexicon-of-idiomatic-expressions/). 

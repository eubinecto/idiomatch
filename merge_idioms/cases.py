"""
Just some constants that must be defined manually
"""
# to be used when building idiom patterns
PRP_PLACEHOLDER_CASES = ('one\'s', 'someone\'s')
PRON_PLACEHOLDER_CASES = ('someone',)
OPTIONAL_CASES = (
    ",",  # comma is optional
    "a", "an", "the"  # articles are optional
)

# this follows the syntax for spacy's tokenization rules
TOKENISATION_CASES = {
    "one's": [{"ORTH": "one's"}],
    "someone's": [{"ORTH": "someone's"}],
    # TODO: is this really the only way?
    "catch-22": [{"ORTH": "catch"}, {"ORTH": "-"}, {"ORTH": "22"}],
    "Catch-22": [{"ORTH": "Catch"}, {"ORTH": "-"}, {"ORTH": "22"}],  # also need a capitalised case.

}

# to be used in loaders.py - the exceptions & additions
IGNORED_CASES = (
    "if needs be",  # duplicate ->  "if need be" is enough. pattern matching with lemmas will cover this case.
    "ride the ... train"  # doesn't have a dedicated wiktionary entry.
)
MORE_CASES = (
    # need this to avoid overlapping match of "come down to" & "down-to-earth"
    "come down to Earth",
    "beat around the bush",  # this is frequently used, but not included in Slide.
)

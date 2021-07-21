"""
Just some constants that must be defined manually
"""
# to be used when building idiom patterns
PRP_PLACEHOLDER_CASES = ["one's", "someone's"]
PRON_PLACEHOLDER_CASES = ['someone', 'something']
OPTIONAL_CASES = [
    ",",  # comma is optional
]

# this follows the syntax for spacy's tokenization rules
SPECIAL_TOK_CASES = {
    "one's": [{"ORTH": "one's"}],
    "someone's": [{"ORTH": "someone's"}],
    # TODO: is this really the only way?
    "catch-22": [{"ORTH": "catch"}, {"ORTH": "-"}, {"ORTH": "22"}],
    "Catch-22": [{"ORTH": "Catch"}, {"ORTH": "-"}, {"ORTH": "22"}],  # also need a capitalised case.

}


# to be used in loaders.py - the exceptions & additions
IGNORED_CASES = [
    "Number Ten",  # duplicate ->  Number 10 exists.
    "if needs be",  # duplicate ->  "if need be" is enough. pattern matching with lemmas will cover this case.
    "ride the ... train",  # doesn't have a dedicated wiktionary entry.
    "above and beyond the call of duty",  # the page has been deleted.
    "be absorbed by",  # this one is also deleted
]

# add more idioms here.
MORE_IDIOM_CASES = [
    "have blood on one's hands",
    "come down to Earth",
    "beat around the bush"
]

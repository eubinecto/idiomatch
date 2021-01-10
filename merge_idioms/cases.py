"""
Just some constants that must be defined manually
"""

# to be used in components.py - the special cases
PSS_PLACEHOLDER_CASES = ('one\'s', 'someone\'s')

# this follows the syntax for spacy's tokenization
TOKENISATION_CASES = {
    "one's": [{"ORTH": "one's"}],
    "someone's": [{"ORTH": "someone's"}],
    "catch-22": [{"ORTH": "catch"}, {"ORTH": "-"}, {"ORTH": "22"}]
}


# to be used in loaders.py - the exceptions
IGNORED_CASES = (
    "if needs be"  # duplicate ->  "if need be" is enough.
)


# TODO: there must be more cases other than this. How do I automatically define correction rules?
CORRECTION_CASES = {
    # it is more used in the latter form.
    "have blood on one's hands": "have one's blood on one's hands"
}

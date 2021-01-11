"""
Just some constants that must be defined manually
"""

# to be used in components.py - the special cases
PSS_PLACEHOLDER_CASES = ('one\'s', 'someone\'s')

# this follows the syntax for spacy's tokenization
TOKENISATION_CASES = {
    "one's": [{"ORTH": "one's"}],
    "someone's": [{"ORTH": "someone's"}],
    # TODO: is this really the only way?
    "catch-22": [{"ORTH": "catch"}, {"ORTH": "-"}, {"ORTH": "22"}],
    "Catch-22": [{"ORTH": "Catch"}, {"ORTH": "-"}, {"ORTH": "22"}]  # also need a capitalised case.

}


# to be used in loaders.py - the exceptions
IGNORED_CASES = (
    "if needs be",  # duplicate ->  "if need be" is enough. pattern matching with lemmas will cover this case.
)


# TODO: there must be more cases other than this. How do I automatically define correction rules?
CORRECTION_CASES = {
    # it is more often used in the latter form.
    "have blood on one's hands": "have one's blood on one's hands",
    # as for french, people just type them in english.
    "pièce de résistance": "piece de resistance",
    "crème de la crème": "creme de la creme",
    # to avoid clashes with somewhere along the line
    "along the lines": "along the line"
}

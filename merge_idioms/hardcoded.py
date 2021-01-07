"""
Just some constants that must be defined manually
"""

# to be used in components.py - the special cases
POSS_HOLDERS = ['one\'s', 'someone\'s']
SPECIAL_CASES = {
    "one's": [{"ORTH": "one's"}],
    "someone's": [{"ORTH": "someone's"}],
    "catch-22": [{"ORTH": "catch"}, {"ORTH": "-"}, {"ORTH": "22"}]
}


# to be used in loaders.py - the exceptions

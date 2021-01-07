from setuptools import setup

setup(
    # the distribution name
    name='merge_idioms',
    entry_points={
        'spacy_factories': [
            # factory = [module]:[class]
            'merge_idioms = components:MergeIdiomsComponent'
         ]
    }
)

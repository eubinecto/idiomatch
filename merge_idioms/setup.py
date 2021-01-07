from setuptools import setup

setup(
    # the distribution name
    name='merge_idioms',
    entry_points={
        'spacy_factories': [
            # factory = [module]:[class]
            'add_special_cases = components:AddSpecialCasesComponent',
            'merge_idioms = components:MergeIdiomsComponent'
         ]
    }
)

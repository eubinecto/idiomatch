from setuptools import setup, find_packages

setup(
    name='merge_idioms',
    version='0.0.10',
    description='spacy pipeline component for merging idioms',
    url='https://github.com/eubinecto/merge-idioms',
    author='Eu-Bin KIM',
    python_requires='>=3.6',
    author_email='tlrndk123@gmail.com',
    license='MIT LICENSE',
    # this is needed to include the subdirectories in the library
    # will include all subdirectories that include __init__.py file.
    # https://stackoverflow.com/a/43254082
    packages=find_packages(),
    install_requires=[
        'spacy-nightly>=3.0.0rc2',
    ],
    entry_points={
        'spacy_factories': [
            # factory = [module]:[class]
            'add_special_cases = merge_idioms.components:AddSpecialCasesComponent',
            'merge_idioms = merge_idioms.components:MergeIdiomsComponent'
         ]
    },
    # include the patterns and target idioms.
    package_data={
        'merge_idioms': ['resources/idiom_patterns.json', 'resources/target_idioms.txt']
    }
)

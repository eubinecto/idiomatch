from setuptools import setup, find_packages

setup(
    name='identify-idioms',
    version='0.0.14',
    description='spacy pipeline component for identifying idioms',
    url='https://github.com/eubinecto/identify-idioms',
    author='Eu-Bin KIM',
    python_requires='>=3.6',
    author_email='tlrndk123@gmail.com',
    license='MIT LICENSE',
    # this is needed to include the subdirectories in the library
    # will include all subdirectories that include __init__.py file.
    # https://stackoverflow.com/a/43254082
    packages=find_packages(),
    install_requires=[
        'spacy>=3.0.1',  # 3.0 is now officially supported
        'bs4>=0.0.1'
    ],
    entry_points={
        'spacy_factories': [
            # factory = [module]:[class]
            'merge_idioms = identify_idioms.components:MergeIdiomsComponent'
         ]
    },
    # include the patterns and target idioms.
    package_data={
        'identify_idioms': ['resources/idiom_patterns.tsv', 'resources/idioms.tsv']
    }
)

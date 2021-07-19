from spacy.matcher.matcher import Matcher


class IdiomMatcher(Matcher):
    """
    a matcher class for.. matching idioms.
    """

    def add_idiom(self, idiom: str):
        """
        Build patterns for the given idiom and add the patterns into the matcher.
        """
        pass

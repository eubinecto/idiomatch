import codecs
import pickle
from typing import List, Optional
from spacy.matcher import Matcher
from spacy.tokens.doc import Doc
from spacy.vocab import Vocab


class MergeIdiomComponent:
    """
    this is essentially the heart of this repository
    """

    def __init__(self, idiom_matcher_str: str):
        # these..must be json serializable
        self.idiom_matcher_str = idiom_matcher_str

    def __call__(self, doc: Doc) -> Doc:
        # use lowercase version of the doc.
        idiom_matcher = self.construct_idiom_matcher()
        matches = idiom_matcher(doc)
        matches = self.normalize(matches, idiom_matcher.vocab)
        for vocab_id, start, end in matches:
            # get back the lemma for this match
            # note: matcher has references to the vocab on its own!
            idiom_lemma = idiom_matcher.vocab.strings[vocab_id]
            # retokenise
            with doc.retokenize() as retokeniser:
                # try:
                retokeniser.merge(doc[start:end],
                                  # set tag as idiom
                                  # TODO: make sure you give it vocab_id.
                                  attrs={'LEMMA': idiom_lemma, 'TAG': 'IDIOM'})
                # except ValueError as ve:
                #     print("pass merging for:" + match_lemma)
                #     pass
        return doc

    def construct_idiom_matcher(self) -> Matcher:
        # create a new instance here
        # have to do make this every single time
        # because matcher is not JSON serializable.
        idiom_matcher = pickle.loads(codecs.decode(self.idiom_matcher_str.encode(), "base64"))
        return idiom_matcher

    # need this to fix the duplicate issue.
    @staticmethod
    def normalize(matches: List[Optional[tuple]], vocab: Vocab) -> List[tuple]:
        """
        have to do this to prevent the case like:
        e.g.
        It's not the end of the world;
        -> will match both "end of the world" and "not the end of the world"
        In such cases, we'd better leave out the superset.
        """
        # first, find the subset
        to_del: List[int] = list()
        for i, match_i in enumerate(matches):
            lemma_i = vocab.strings[match_i[0]]
            for j, match_j in enumerate(matches):
                lemma_j = vocab.strings[match_j[0]]
                if j != i:  # only if they are different
                    if lemma_j in lemma_i:
                        to_del.append(j)
        else:
            for del_idx in to_del:
                # delete the reference to the items
                # not necessarily the items itself.
                matches[del_idx] = None
            else:
                return [
                    match
                    for match in matches
                    if match
                ]

    # factory method for the component
    @staticmethod
    def create_merge_idiom_component(nlp, name, idiom_matcher_str: str) -> 'MergeIdiomComponent':
        return MergeIdiomComponent(idiom_matcher_str)

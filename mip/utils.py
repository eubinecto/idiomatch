from typing import List
from spacy import Language
from spacy.matcher import Matcher
from spacy.tokens.doc import Doc


class MergeIdiomComponent:
    def __init__(self, idiom_matcher):
        self.idiom_matcher: Matcher = idiom_matcher

    def __call__(self, doc: Doc) -> Doc:
        # use lowercase version of the doc.
        matches = self.idiom_matcher(doc)
        self.del_subset(matches)
        for match_id, start, end in matches:
            # get back the lemma for this match
            # note: matcher has references to the vocab on its own!
            match_lemma = self.idiom_matcher.vocab.strings[match_id]
            # retokenise
            with doc.retokenize() as retokeniser:
                # try:
                retokeniser.merge(doc[start:end],
                                  # set tag as the idiom
                                  attrs={'LEMMA': match_lemma, 'TAG': 'IDIOM'})
                # except ValueError as ve:
                #     print("pass merging for:" + match_lemma)
                #     pass
        return doc

    # need this to fix the duplicate issue.
    def del_subset(self, matches: List[tuple]):
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
            lemma_i = self.idiom_matcher.vocab.strings[i]
            for j, match_j in enumerate(matches):
                lemma_j = self.idiom_matcher.vocab.strings[j]
                if j != i:
                    if lemma_j in lemma_i:
                        to_del.append(j)
        else:
            for del_idx in to_del:
                matches.pop(del_idx)


class MergeIdiomPipeline:
    def __init__(self, nlp: Language, idiom_matcher: Matcher):
        self.nlp = nlp
        self.idiom_matcher = idiom_matcher
        # factory for merge_idiom pipeline.
        Language.factory(
            name="merge_idiom",
            retokenizes=True,  # we are merging, so it does retokenizes stuff.
            default_config={"idiom_matcher": self.idiom_matcher},
            func=MergeIdiomPipeline.create_merge_idiom_component
        )
        # add the pipe, and save it to disk
        nlp.add_pipe("merge_idiom", after="lemmatizer")

    def __call__(self, text: str, *args, **kwargs):
        # just a wrapper, to construct the pipeline on init.
        # I know that you'd lose some information here.. (Kate -> kate. NOT Proper Noun anymore, just a Noun).
        # but, we've got to make a compromise here.
        # TODO: Is there a way I can do this without .lower?
        return self.nlp(text.strip().lower())

    # factory method for the component
    @staticmethod
    def create_merge_idiom_component(nlp, name, idiom_matcher) -> MergeIdiomComponent:
        if not idiom_matcher:
            raise ValueError("idiom_matcher does not exist.")
        return MergeIdiomComponent(idiom_matcher)

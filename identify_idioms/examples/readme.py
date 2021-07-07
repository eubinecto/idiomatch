from identify_idioms.service import build_iip


def main():

    sentences = [
        "You are down to earth.",
        "Have you found your feet on the new job?",
        "To ask our members to accept a pay cut heaps insult on injury."
    ]
    # build a spacy pipeline for merging idioms, based off of en_core_web_sm model
    iip = build_iip()

    for sent in sentences:
        # process the sentence
        doc = iip(sent)
        # idioms are identified as atomic tokens in tokenisation process
        token_texts = [token.text for token in doc]
        # supports lemmatization of idioms as well
        token_lemmas = [token.lemma_ for token in doc]
        # is_idiom custom attribute can be used to filter idioms
        token_idioms = [token.lemma_ for token in doc if token._.is_idiom]

        print("tokenisation:", token_texts)
        print("lemmatisation:", token_lemmas)
        print("filtering:", token_idioms)
        print("-----------")


if __name__ == '__main__':
    main()

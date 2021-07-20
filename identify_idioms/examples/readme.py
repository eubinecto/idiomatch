import spacy
from identify_idioms import IdiomMatcher


def main():

    sentences = [
        "You are down to earth.",
        "Have you found your feet on the new job?",
    ]

    nlp = spacy.load("en_core_web_sm")  # idiom matcher needs an nlp pipeline. Currently supports en_core_web_sm only.
    idiom_matcher = IdiomMatcher.from_pretrained(nlp)  # this will take approx 40 seconds.

    for sent in sentences:
        # process the sentence
        doc = nlp(sent)
        # identify all
        matches = idiom_matcher(doc)
        for token_id, start, end in matches:
            print(nlp.vocab.strings[token_id], start, end)
        print("-----")


if __name__ == '__main__':
    main()

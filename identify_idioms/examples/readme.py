import spacy
import pprint
from identify_idioms import IdiomMatcher


def main():

    sentences = [
        "You are down to earth",
        "Have you found your feet on the new job?",
        "If she dies, you have her blood is on your hands!"
    ]

    nlp = spacy.load("en_core_web_sm")  # idiom matcher needs an nlp pipeline. Currently supports en_core_web_sm only.
    idiom_matcher = IdiomMatcher.from_pretrained(nlp)  # this will take approx 40 seconds.

    for sent in sentences:
        print("\n### {} ###".format(sent))
        doc = nlp(sent)  # process the sentence
        res = idiom_matcher.identify(doc)  # identify all idioms
        pprint.PrettyPrinter().pprint(res)  # pretty print the json result


if __name__ == '__main__':
    main()
